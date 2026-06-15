# Implementation Plan: Create Reservations List per Class Slot

**Branch**: `008-reservation-lists` | **Date**: 2026-06-14 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/008-reservations-list-per-class/spec.md`

## Summary

Add a reservations list page for Operators and Administrators to view equipment-to-client assignments for a given class slot and date, with PDF export. The list shows active reservations in a table ordered by equipment name. Additionally, the main Reservations page (`/reservations/`) is updated with a class slot filter and displays the per-slot equipment-client table when both class slot and date are selected.

## Technical Context

**Language/Version**: Python 3.12, Django 5.0.x

**Primary Dependencies**: Django, psycopg2-binary, gunicorn, whitenoise

**Storage**: PostgreSQL 16 (Docker) / SQLite3 (local fallback)

**Testing**: pytest, pytest-django

**Target Platform**: Linux server (Docker container)

**Project Type**: Web application (Django server-rendered, Bootstrap 5.3.3 + HTMX 2.0.4)

**Performance Goals**: List renders in <2s for up to 50 reservations; PDF export completes in <5s

**Constraints**: Existing Django ORM models; no REST API; all labels MUST use Django i18n (`gettext`/`gettext_lazy`) with Spanish translations; UI must follow Bootstrap 5 patterns

**Scale/Scope**: Internal gym management tool, single-tenant, ≤50 reservations per class slot per date

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment |
|-----------|------------|
| I. Code Quality | **PASS** — No new dependencies or architectural complexity. Existing linting (Ruff) and review process apply. |
| II. Testing Standards | **PASS** — TDD required. View-level tests for the list page and PDF export. PDF mocking permissible for tests. Integration test for end-to-end flow. |
| III. UX Consistency | **PASS** — Follows existing Bootstrap 5 patterns. All new labels use Django i18n (`gettext_lazy`). Error messages actionable. List supports human-readable and export (PDF) output. |
| IV. Performance | **PASS** — SC-002 (2s load) and SC-003 (5s export) defined in spec. No anticipated regressions. |

No violations — Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
specs/008-reservations-list-per-class/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── README.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/     # Existing app — new views for reservation list
│       ├── models.py     # Existing Reservation model
│       ├── views.py      # + reservation_list, reservation_list_pdf
│       ├── urls.py       # + new URL patterns
│       └── templates/
│           └── reservations/
│               ├── reservation_list.html      # Modified: class slot filter + per-slot table
│               ├── reservation_list_by_slot.html  # New: per-slot list page
│               └── reservation_list_pdf.html  # New: PDF template
├── templates/
│   └── base.html         # Shared Bootstrap 5 layout
└── tests/
    ├── test_reservations_list.py  # New: list + PDF tests
    └── ... existing test files
```

**Structure Decision**: Single Django project (`backend/`) with a new view in the existing `reservations` app. No new apps needed. PDF export uses Django's `render_to_string` + `WeasyPrint` or browser print-to-PDF approach.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations — this section intentionally left blank.
