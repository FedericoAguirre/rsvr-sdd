import io
import calendar
import json
from datetime import date, datetime

from apps.classes.models import ClassSlot
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from apps.classes.models import ClassSlot

from .forms import ReservationForm
from .models import Reservation

logger = logging.getLogger(__name__)


def _get_slot_reservations(class_slot_pk, date_str):
    reservations = Reservation.objects.none()
    class_slot = None
    if class_slot_pk and date_str:
        reservations = Reservation.objects.filter(
            class_slot_id=class_slot_pk,
            date=date_str,
        ).select_related("client", "equipment", "class_slot").order_by("equipment__name")
        class_slot = get_object_or_404(ClassSlot, pk=class_slot_pk)
    return reservations, class_slot


@login_required
def reservation_list_pdf(request):
    class_slot_pk = request.GET.get("class_slot")
    date_str = request.GET.get("date", "")
    reservations, class_slot = _get_slot_reservations(class_slot_pk, date_str)
    date_display = date_str.replace("-", "/") if date_str else ""
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            topMargin=2 * cm, bottomMargin=2 * cm,
            leftMargin=2 * cm, rightMargin=2 * cm,
        )
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(_("Reservations by Class"), styles["h2"]))
        elements.append(Spacer(1, 0.5 * cm))
        header_text = f"<b>{_('Date')}:</b> {date_display} &mdash; <b>{_('Class')}:</b> {class_slot}"
        elements.append(Paragraph(header_text, styles["Normal"]))
        elements.append(Spacer(1, 0.5 * cm))

        if reservations:
            data = [[
                Paragraph(_("Equipment"), styles["Normal"]),
                Paragraph(_("Client"), styles["Normal"]),
                Paragraph(_("Status"), styles["Normal"]),
            ]]
            for r in reservations:
                data.append([
                    Paragraph(r.equipment.name, styles["Normal"]),
                    Paragraph(" ".join(p for p in [r.client.first_name, r.client.last_name] if p), styles["Normal"]),
                    Paragraph(r.get_status_display(), styles["Normal"]),
                ])
            col_widths = [doc.width * 0.35, doc.width * 0.40, doc.width * 0.25]
            table = Table(data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ]))
            elements.append(table)
        else:
            elements.append(Paragraph(
                _("No reservations found for this class and date."),
                styles["Normal"],
            ))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf, content_type="application/pdf")
        safe_name = (
            str(class_slot).replace(" ", "_").translate(
                str.maketrans("", "", "/" + chr(0) + '<>:"|?*')
            ) if class_slot else "unknown"
        )
        date_compact = date_str.replace("-", "") if date_str else "no_date"
        filename = f"reservations_{safe_name}_{date_compact}.pdf"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
    except Exception as exc:
        logger.exception("PDF generation failed: %s", exc)
        messages.error(request, _("Could not generate the PDF. Please try again."))
        return redirect(request.META.get("HTTP_REFERER", "reservations:reservation-list"))


@login_required
def reservation_list(request):
    date_str = request.GET.get("date", "")
    class_slot_pk = request.GET.get("class_slot", "")
    status_filter = request.GET.get("status", "")
    if class_slot_pk and date_str:
        reservations, class_slot = _get_slot_reservations(class_slot_pk, date_str)
    else:
        reservations = Reservation.objects.select_related("client", "equipment", "class_slot").all()
        if date_str:
            reservations = reservations.filter(date=date_str)
        class_slot = None
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    class_slots = ClassSlot.objects.all()
    today = timezone.localdate()
    date_display = date_str.replace("-", "/") if date_str else ""
    return render(request, "reservations/reservation_list.html", {
        "reservations": reservations,
        "today": today,
        "class_slots": class_slots,
        "class_slot": class_slot,
        "date_str": date_str,
        "date_display": date_display,
        "status_filter": status_filter,
    })


@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(
        Reservation.objects.select_related("client", "equipment", "class_slot", "created_by"),
        pk=pk,
    )
    return render(request, "reservations/reservation_detail.html", {"reservation": reservation})


@login_required
def reservation_change_status(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    new_status = request.POST.get("status")
    if new_status is None and request.headers.get("Content-Type") == "application/json":
        try:
            new_status = json.loads(request.body).get("status")
        except (json.JSONDecodeError, AttributeError):
            new_status = None
    valid_statuses = dict(Reservation.STATUS_CHOICES)
    if new_status not in valid_statuses:
        if request.headers.get("HX-Request"):
            return HttpResponse(_("Invalid status."), status=400)
        messages.error(request, _("Invalid status."))
        return redirect("reservations:reservation-detail", pk=reservation.pk)
    reservation.status = new_status
    reservation.save()
    if request.headers.get("HX-Request"):
        response = render(request, "reservations/partials/reservation_row.html", {
            "reservation": reservation,
        })
        response["HX-Trigger"] = "statusChanged"
        return response
    messages.success(request, _("Reservation status updated."))
    return redirect("reservations:reservation-detail", pk=reservation.pk)


def auto_date_for_slot(selected_slot_id):
    """Calculate the auto-date for a given class slot based on today's date/time."""
    try:
        slot = ClassSlot.objects.get(pk=selected_slot_id, is_active=True)
    except ClassSlot.DoesNotExist:
        return None
    today = date.today()
    now = datetime.now().time()
    slot_day = slot.day_of_week
    today_day = today.weekday()  # 0=Mon..4=Fri
    days_ahead = slot_day - today_day + 7
    result = date.fromordinal(today.toordinal() + days_ahead)
    return result.isoformat()


@login_required
def reservation_create(request):
    initial = {}
    client_pk = request.GET.get("client")
    if client_pk:
        initial["client"] = client_pk
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.created_by = request.user
            reservation.save()
            messages.success(request, _("Reservation created."))
            return redirect("reservations:reservation-detail", pk=reservation.pk)
    else:
        form = ReservationForm(initial=initial)
    slots_qs = ClassSlot.objects.filter(is_active=True).values("id", "day_of_week", "time")
    slots_data = [{
        "id": s["id"],
        "day_of_week": s["day_of_week"],
        "time": s["time"].strftime("%H:%M"),
    } for s in slots_qs]
    return render(request, "reservations/reservation_form.html", {
        "form": form,
        "slots_data": slots_data,
    })
