# Research: Export Payments

## Technology Decisions

### Decision: openpyxl for .xlsx generation

- **Rationale**: openpyxl is the de-facto standard for reading/writing Excel .xlsx files in Python. It supports write-only mode for memory-efficient large exports (streaming), full formatting control, and produces files compatible with Excel, LibreOffice Calc, and Google Sheets.
- **Alternatives considered**:
  - **xlwt**: Legacy, .xls only (not .xlsx), no longer maintained
  - **XlsxWriter**: Supports .xlsx but only writes (no reading), no streaming support
  - **csv**: Not .xlsx format; violates acceptance criteria which explicitly specifies .xlsx
  - **pandas**: Heavy dependency for a simple columnar export; overkill for this use case
  - **tablib** (used by django-import-export): Adds abstraction layer with marginal benefit for a single export endpoint

### Decision: Extend existing PaymentReportView

- **Rationale**: The spec (FR-007) explicitly requires reuse of existing payments/reports views and logic. The date range filter and query logic already exist in `PaymentReportView`. Adding a new `PaymentExportView` that reuses the same query logic keeps the code DRY.
- **Alternatives considered**:
  - **New standalone view**: Would duplicate query logic — rejected per FR-007
  - **Async background job**: Adds complexity (Celery/redis) unjustified for typical <10k row datasets

### Decision: Write-only mode for streaming large exports

- **Rationale**: openpyxl's `write_only=True` mode streams rows without keeping the entire workbook in memory. This handles arbitrarily large datasets gracefully as confirmed in the clarifications session.
- **Alternatives considered**:
  - **Default in-memory mode**: Risk of OOM for large datasets; acceptable for <10k rows but not for unbounded streaming

### Decision: i18n for all user-facing strings

- **Rationale**: Constitution mandates i18n as non-negotiable with zero exceptions. Button label "Exportar", alert messages, validation errors, and error messages all require i18n entries in `django.po` (Spanish locale).

## Existing Patterns

### PDF Export (ReportLab) — reference for implementation pattern

The existing `reservation_list_pdf` view in `backend/apps/reservations/views.py` follows this pattern:

1. Build in-memory buffer (`io.BytesIO()`)
2. Generate document content into buffer
3. Create `HttpResponse` with appropriate content type
4. Set `Content-Disposition: attachment; filename="..."`
5. Return response
6. Catch exceptions, log, redirect with error message

The xlsx export will follow the same pattern, substituting openpyxl for ReportLab.

### CSV Import — reference for non-PDF file handling

`backend/apps/clients/csv_import.py` demonstrates the project's pattern for file I/O with Django models.

## Dependencies

- **openpyxl** (new): Must be added to `pyproject.toml`
- **reportlab** (existing): No changes needed; used only as reference pattern
