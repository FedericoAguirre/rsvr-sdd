# Implementation Plan: Rename Exported Reservations PDF

**Branch**: `010-pdf-export-filename` | **Date**: 2026-06-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/010-pdf-export-filename/spec.md`

## Summary

Change the exported Reservations PDF filename from `reservations-2026-06-15.pdf` to `reservations_Morning_Yoga_20260615.pdf`, including the sanitized class slot name and compact date format.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.x, WeasyPrint (PDF generation), django.i18n (translations)

**Storage**: PostgreSQL (data layer, unchanged by this feature)

**Testing**: Django TestCase (existing pattern in `backend/tests/test_reservations_list.py`)

**Target Platform**: Linux x86_64 (Docker container — `python:3.12-slim`)

**Project Type**: Web application (Django monolith, single backend)

**Performance Goals**: PDF generation completed within 5 seconds (existing metric from SC-003). Filename change adds no measurable overhead.

**Constraints**: Filenames must be filesystem-safe across Windows/macOS/Linux (no `/`, `\0`, control characters). Existing PDF content/formatting unchanged.

**Scale/Scope**: Single-file change to `backend/apps/reservations/views.py`. No data model, UI, or infrastructure changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Code Quality | ✅ PASS | Small change, will pass linting. No complexity added — single-line filename format change. |
| II. Testing Standards (NON-NEGOTIABLE) | ✅ PASS | Existing PDF export test can be updated to assert new filename format. No new contracts or inter-module boundaries crossed. |
| III. User Experience Consistency | ✅ PASS | Filename follows consistent naming pattern. Spanish i18n labels already applied in PDF template — no label changes needed. |
| IV. Performance Requirements | ✅ PASS | Filename change has zero performance impact. Existing ~5s PDF generation metric unaffected. |
| Technology Constraints | ✅ PASS | No new dependencies introduced. |
| Development Workflow | ✅ PASS | Sequential branch name (010-pdf-export-filename). Atomic commit expected. |

No violations found. Complexity Tracking section omitted.

## Project Structure

### Documentation (this feature)

```text
specs/010-pdf-export-filename/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A — no data model change)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A — no interface change)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── views.py              # [MODIFY] filename format in Content-Disposition
│       └── urls.py               # (unchanged)
└── tests/
    └── test_reservations_list.py # [MODIFY] update assertion on filename
```

**Structure Decision**: Django web application — single backend project under `backend/`. Only `views.py` requires modification; tests updated in `test_reservations_list.py`.
