# Research: Create Reservations List per Class Slot

## Decisions

### PDF generation approach

- **Decision**: Use WeasyPrint for server-side PDF generation from an HTML template
- **Rationale**: WeasyPrint renders HTML+CSS to PDF with high fidelity, supports Bootstrap-like styling, and produces a downloadable file without relying on browser print dialogs. The Docker image can be extended with the required system libraries (`libpango-1.0-0`, `libcairo2`, `libgdk-pixbuf2.0-0`) without significant bloat.
- **Alternatives considered**:
  - Browser print-to-PDF (`window.print()`) — simplest approach, zero dependencies, but gives the user a print dialog instead of a direct download, and PDF formatting varies by browser
  - xhtml2pdf — Django-compatible but has poor CSS support and would require template rework
  - ReportLab — programmatic generation, verbose, no HTML/CSS reuse
  - django-wkhtmltopdf — wrapper around wkhtmltopdf, requires a headless browser binary (large)

### URL structure for the new page

- **Decision**: `/reservations/list/?class_slot=<id>&date=<YYYY-MM-DD>` for the view, `/reservations/list/pdf/?class_slot=<id>&date=<YYYY-MM-DD>` for PDF export
- **Rationale**: Matches existing URL conventions in the app (query parameters for filters). The PDF variant reuses the same data query with a different template.
- **Alternatives considered**: POST-based form submission — less bookmarkable and harder to test

### Filtering logic

- **Decision**: Query `Reservation` model filtered by `class_slot`, `date`, and `status='active'` (or equivalent), ordered by `equipment__name`
- **Rationale**: Matches existing Reservation model which has FK to ClassSlot, DateField for date, and can be extended with a status field. Ordering by equipment name fulfills FR-004.
- **Alternatives considered**: Filtering cancelled/expired in template — less efficient, couples display logic to data concerns

## No unresolved items

All technical decisions aligned with project conventions and spec requirements. No NEEDS CLARIFICATION markers remain after the clarification session.
