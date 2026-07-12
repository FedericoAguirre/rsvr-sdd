# Implementation Plan: Replace WeasyPrint with ReportLab for Cross-Platform PDF

**Branch**: `038-replace-weasyprint-pdf` | **Date**: 2026-07-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/038-replace-weasyprint-pdf/spec.md`

## Summary

Replace the WeasyPrint PDF engine in the reservations PDF view with ReportLab to enable cross-platform PDF generation (Linux/macOS/Windows) without system-level dependencies. The PDF output preserves the same data fields and visual structure (table with borders, readable fonts) while removing WeasyPrint from project dependencies and the Dockerfile.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.0.x, ReportLab >=4.0, psycopg2-binary, gunicorn, whitenoise

**Storage**: PostgreSQL (unchanged by this feature)

**Testing**: pytest + pytest-django (Django TestCase). Existing test at `backend/tests/test_reservations_list.py` contains PDF tests that need updating.

**Target Platform**: Linux x86_64 (Docker container — `python:3.12-slim`), macOS, Windows

**Project Type**: Web application (Django monolith, single backend)

**Performance Goals**: PDF generation completed within 10 seconds for reservation lists of up to 100 entries (SC-004)

**Constraints**: Must not require any system-level packages (libpango, libcairo, libgdk-pixbuf). All user-visible strings in the PDF MUST use Django i18n (constitution requirement — non-negotiable). Non-ASCII characters (Spanish accents, ñ) must render correctly.

**Scale/Scope**: Single view change in `backend/apps/reservations/views.py` (`reservation_list_pdf`). No data model, UI, or other infrastructure changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Code Quality | ✅ PASS | Single view replacement. No added complexity — one library swap with equivalent API surface. No dead code, no YAGNI violations. |
| II. Testing Standards (NON-NEGOTIABLE) | ✅ PASS w/ conditions | Existing PDF tests need migration to ReportLab assertions. Integration test required for library contract change (WeasyPrint → ReportLab). TDD: tests must be written and reviewed before implementation. |
| III. User Experience Consistency | ✅ PASS w/ conditions | PDF filename unchanged. All user-visible strings in PDF MUST use Django i18n (`{% translate %}` → `gettext()`). The existing HTML template uses i18n — ReportLab code must do the same. |
| IV. Performance Requirements | ✅ PASS | SC-004 sets 10s for 100 entries — well within ReportLab's capabilities. No performance regression expected. |

## Project Structure

### Documentation (this feature)

```text
specs/038-replace-weasyprint-pdf/
├── plan.md              # This file
├── research.md          # ReportLab research findings
├── data-model.md        # PDF output structure
├── quickstart.md        # Migration guide
├── contracts/           # CLI contract (unchanged)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── views.py              # [MODIFY] reservation_list_pdf view
│       └── templates/
│           └── reservations/
│               └── reservation_list_pdf.html  # [DELETE] HTML template no longer needed
├── pyproject.toml                 # [MODIFY] weasyprint → reportlab dependency
├── Dockerfile                     # [MODIFY] remove system deps (libpango, libcairo, etc.)
└── tests/
    └── test_reservations_list.py  # [MODIFY] update PDF tests
```

**Structure Decision**: Single Django project. All changes are contained within the `reservations` app and top-level config files.

## Complexity Tracking

None required — single library swap, no architectural complexity added.

## Phase 0: Research

### Unknowns Resolved

| Unknown | Resolution | Source |
|---------|-----------|--------|
| ReportLab API for table PDF generation | ReportLab's `platypus` framework (`SimpleDocTemplate`, `Table`, `TableStyle`, `Paragraph`) is the standard approach | Research |
| i18n integration with ReportLab | Django's `gettext()` is called in Python before passing strings to ReportLab. No template rendering needed. | Research |
| Non-ASCII font support | ReportLab includes built-in fonts (Helvetica, Times-Roman, Courier) that support Latin-1. For Spanish (ñ, accents), Latin-1 / win-1252 encoding is sufficient without external fonts. | Research |
| Automatic pagination | `SimpleDocTemplate` handles page breaks automatically. `Table` with `repeatRows` for header on each page. | Research |

### Research Tasks

1. Investigate ReportLab `platypus` (Page Layout and Typography Using Scripts) for table-based PDF generation
2. Confirm ReportLab >=4.0 installs via pip on all three target OS without system packages
3. Validate Latin-1 encoding handles Spanish characters (ñ, á, é, í, ó, ú) with built-in fonts
4. Research test strategy: validate PDF content by extracting text from generated PDF vs. snapshot
