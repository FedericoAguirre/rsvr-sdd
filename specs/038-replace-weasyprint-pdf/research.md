# Research: Replace WeasyPrint with ReportLab

## Decision: Use ReportLab `platypus` for PDF generation

**Rationale**: ReportLab's `platypus` (Page Layout and Typography Using Scripts) framework provides `SimpleDocTemplate`, `Table`, `TableStyle`, and `Paragraph` objects that are the standard approach for programmatic PDF generation in Python. The API maps cleanly to the current HTML table structure.

**Alternatives considered**:
- WeasyPrint (current): Requires system libraries (libpango, libcairo, libgdk-pixbuf) — fails on macOS/Windows without special setup
- pdfkit/wkhtmltopdf: Requires wkhtmltopdf binary — same platform dependency problem
- FPDF2: Lighter weight but lacks table layout and pagination features of ReportLab
- xhtml2pdf: Converts HTML+CSS but has limited CSS support and rendering quirks

## Decision: ReportLab >=4.0 as dependency

**Rationale**: ReportLab 4.0+ is pure Python, installs via pip on all platforms, and has no system-level dependencies. Available on PyPI.

**Installation**: `uv add reportlab>=4.0`

**Platform testing verified**:
- Linux (python:3.12-slim): ✅ No system packages needed
- macOS (arm64): ✅ pip install only
- Windows: ✅ pip install only

## Decision: Django `gettext()` for i18n

**Rationale**: ReportLab does not have built-in i18n support. All user-visible strings (title, column headers, empty state message) are passed as Python strings. Django's `gettext()` function is called at render time:

```python
from django.utils.translation import gettext as _

title = _("Reservations by Class")
column_headers = [_("Equipment"), _("Client"), _("Status")]
empty_msg = _("No reservations found for this class and date.")
```

This ensures the same translation keys used in the HTML template are preserved.

## Decision: Latin-1 encoding for Spanish character support

**Rationale**: ReportLab's built-in fonts (Helvetica) support Latin-1 (ISO 8859-1) encoding which covers Spanish characters (ñ, á, é, í, ó, ú). No external font files needed.

**Implementation**: Set `pdfmetrics.registerFont(TTFont(...))` only if custom fonts are needed. For Latin-1, built-in fonts suffice.

## Decision: Test via PDF text extraction

**Rationale**: PDF binary comparison is fragile (timestamps, metadata vary). Instead, extract text from the generated PDF and assert content fields present. Use `io.BytesIO` to capture PDF in-memory during tests.

**Approach**:
1. Call `reservation_list_pdf` view with test data
2. Assert response content-type is `application/pdf`
3. Use `PyPDF2` or `pdfminer.six` to extract text from the response content
4. Assert key strings appear: class slot name, date, reservation data (equipment name, client name, status)

**Note**: Adding `pdfminer.six` to dev dependencies for test assertion support (or use ReportLab's own test utilities).

## Edge Cases Covered

| Case | Resolution |
|------|-----------|
| Empty reservation list | Show header row + "No reservations found" message text |
| Non-ASCII names (ñ, accents) | Latin-1 encoded built-in fonts support all Spanish characters |
| Multi-page lists | `SimpleDocTemplate` auto-paginates; `Table` with `repeatRows=1` repeats header |
| PDF generation failure | Existing try/except preserved — logs error, redirects with user message |
| Missing ReportLab | Python `ImportError` at view top — clear error message |

## Key ReportLab API Reference

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors

# Document setup
buffer = io.BytesIO()
doc = SimpleDocTemplate(buffer, pagesize=A4,
                        topMargin=2*cm, bottomMargin=2*cm,
                        leftMargin=2*cm, rightMargin=2*cm)

# Build content
elements = []
styles = getSampleStyleSheet()
elements.append(Paragraph(title, styles["h2"]))
elements.append(Spacer(1, 12))

# Table
data = [["Header1", "Header2", "Header3"]] + row_data
table = Table(data, colWidths=[...])
table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
]))

elements.append(table)
doc.build(elements)
pdf_bytes = buffer.getvalue()
```
