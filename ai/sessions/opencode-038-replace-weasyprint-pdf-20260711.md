# Session: 038 Replace WeasyPrint PDF Generation

**Model**: deepseek-v4-flash (opencode)
**Date**: 2026-07-11
**Branch**: `038-replace-weasyprint-pdf`

## Summary

Replaced WeasyPrint with ReportLab for cross-platform PDF generation. WeasyPrint required system packages (libpango, libcairo, libgdk-pixbuf) that blocked PDF tests on macOS/Windows. ReportLab is pure Python with no system dependencies.

## Key Changes

- **`backend/pyproject.toml`**: Swapped `weasyprint` for `reportlab>=4.0` + `pdfminer.six` (dev)
- **`backend/Dockerfile`**: Removed WeasyPrint system deps (libpango, libcairo, libgdk-pixbuf)
- **`backend/apps/reservations/views.py`**: Rewrote PDF export using ReportLab `platypus` (SimpleDocTemplate, Table, TableStyle, Paragraph) with Django `gettext()` i18n
- **`backend/tests/test_reservations_list.py`**: Updated 4 existing PDF tests + 2 new tests (content assertions via pdfminer.six text extraction)
- **`backend/apps/reservations/templates/reservations/reservation_list_pdf.html`**: Deleted (no longer needed)

## Workflow

Completed full Spec Kit workflow:
1. `/speckit.specify` — spec with 3 user stories
2. `/speckit.clarify` — 2 clarifications (visual fidelity, empty state)
3. `/speckit.plan` — plan, research, data-model, quickstart
4. `/speckit.tasks` — 15 tasks across 5 phases
5. `/speckit.implement` — all 15 tasks executed

## Results

- 35/36 pass in reservations tests (1 pre-existing i18n assertion mismatch)
- 8/8 PDF-specific tests pass
- `uv.lock` regenerated, `uv sync --frozen` successful
