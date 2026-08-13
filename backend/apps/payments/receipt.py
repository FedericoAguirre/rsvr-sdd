"""Build localized payment receipt projections and export formats."""

import io
import re
from pathlib import Path
from xml.sax.saxutils import escape

from django.utils.formats import date_format
from django.utils.translation import gettext as _
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

_UNSAFE_FILENAME = re.compile(r'[\\/:*?"<>|\x00-\x1f]+')
_FONT_NAME = "ReceiptDejaVu"
_FONT_PATHS = (
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
)


def _receipt_font_name():
    if _FONT_NAME in pdfmetrics.getRegisteredFontNames():
        return _FONT_NAME
    for font_path in _FONT_PATHS:
        if font_path.exists():
            pdfmetrics.registerFont(TTFont(_FONT_NAME, str(font_path)))
            return _FONT_NAME
    return "Helvetica"


def _safe_filename_part(value):
    cleaned = _UNSAFE_FILENAME.sub("_", str(value or ""))
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned.strip("_") or "unknown"


def _client_name(client):
    return " ".join(part for part in (client.first_name, client.last_name) if part)


def build_receipt(payment):
    """Return the normalized, localized receipt data for one payment."""
    reservations = list(
        payment.payment_reservations.select_related(
            "reservation__class_slot",
            "reservation__equipment",
        ).order_by("reservation__date", "reservation__class_slot__time")
    )
    client_name = _client_name(payment.client)
    reference = payment.reference or payment.pk
    rows = [
        {
            "class_slot": str(link.reservation.class_slot),
            "date": link.reservation.date.strftime("%d/%m/%Y"),
            "equipment": str(link.reservation.equipment)
            if link.reservation.equipment
            else str(_("Not specified")),
            "status": str(link.reservation.get_status_display()),
        }
        for link in reservations
    ]
    labels = {
        "title": str(_("Payment Receipt")),
        "client": str(_("Client")),
        "amount": str(_("Amount")),
        "payment_type": str(_("Payment type")),
        "date": str(_("Date")),
        "class_slot_count": str(_("Class slot count")),
        "class_slot": str(_("Class Slot")),
        "equipment": str(_("Equipment")),
        "status": str(_("Status")),
        "no_reservations": str(_("No reservations found")),
    }
    return {
        "labels": labels,
        "client": client_name,
        "amount": f"{payment.amount:.2f}",
        "payment_type": str(payment.get_payment_type_display()),
        "date": date_format(payment.date, "SHORT_DATE_FORMAT"),
        "class_slot_count": str(payment.class_slot_count),
        "reference": str(reference),
        "filename": (
            f"payment_{_safe_filename_part(client_name)}_"
            f"{_safe_filename_part(reference)}.pdf"
        ),
        "reservations": rows,
    }


def render_markdown(receipt):
    """Render a receipt projection as copyable Markdown."""
    labels = receipt["labels"]
    lines = [
        f"# {labels['title']}",
        "",
        f"- **{labels['client']}:** {receipt['client']}",
        f"- **{labels['amount']}:** {receipt['amount']}",
        f"- **{labels['payment_type']}:** {receipt['payment_type']}",
        f"- **{labels['date']}:** {receipt['date']}",
        f"- **{labels['class_slot_count']}:** {receipt['class_slot_count']}",
        "",
        (
            f"| {labels['class_slot']} | {labels['date']} | "
            f"{labels['equipment']} | {labels['status']} |"
        ),
        "| --- | --- | --- | --- |",
    ]
    if receipt["reservations"]:
        lines.extend(
            "| {class_slot} | {date} | {equipment} | {status} |".format(**row)
            for row in receipt["reservations"]
        )
    else:
        lines.append(f"| {labels['no_reservations']} | | | |")
    return "\n".join(lines) + "\n"


def render_pdf(receipt):
    """Render a receipt projection as an in-memory PDF."""
    buffer = io.BytesIO()
    font_name = _receipt_font_name()
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReceiptBody",
            parent=styles["Normal"],
            fontName=font_name,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReceiptHeading",
            parent=styles["Heading1"],
            fontName=font_name,
        )
    )
    body = styles["ReceiptBody"]
    heading = styles["ReceiptHeading"]
    labels = receipt["labels"]
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )
    elements = [Paragraph(escape(labels["title"]), heading), Spacer(1, 0.4 * cm)]
    header_rows = [
        (labels["client"], receipt["client"]),
        (labels["amount"], receipt["amount"]),
        (labels["payment_type"], receipt["payment_type"]),
        (labels["date"], receipt["date"]),
        (labels["class_slot_count"], receipt["class_slot_count"]),
    ]
    elements.append(
        Table(
            [
                [
                    Paragraph(f"<b>{escape(label)}:</b>", body),
                    Paragraph(escape(value), body),
                ]
                for label, value in header_rows
            ],
            colWidths=[document.width * 0.35, document.width * 0.65],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            ),
        )
    )
    elements.append(Spacer(1, 0.5 * cm))
    table_data = [
        [
            Paragraph(escape(labels["class_slot"]), body),
            Paragraph(escape(labels["date"]), body),
            Paragraph(escape(labels["equipment"]), body),
            Paragraph(escape(labels["status"]), body),
        ]
    ]
    if receipt["reservations"]:
        table_data.extend(
            [
                Paragraph(escape(row["class_slot"]), body),
                Paragraph(escape(row["date"]), body),
                Paragraph(escape(row["equipment"]), body),
                Paragraph(escape(row["status"]), body),
            ]
            for row in receipt["reservations"]
        )
    else:
        table_data.append(
            [Paragraph(escape(labels["no_reservations"]), body), "", "", ""]
        )
    table = Table(
        table_data,
        colWidths=[
            document.width * 0.29,
            document.width * 0.17,
            document.width * 0.29,
            document.width * 0.25,
        ],
        repeatRows=1,
    )
    table_styles = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if not receipt["reservations"]:
        table_styles.append(("SPAN", (0, 1), (-1, 1)))
    table.setStyle(TableStyle(table_styles))
    elements.append(table)
    document.build(elements)
    return buffer.getvalue()
