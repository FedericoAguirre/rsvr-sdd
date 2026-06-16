# Implementation Plan: Add Reservation Status

**Branch**: `013-reservation-status` | **Date**: 2026-06-15 | **Spec**: `specs/013-reservation-status/spec.md`

**Input**: Feature specification from `/specs/013-reservation-status/spec.md`

## Summary

Add a `status` field to the `Reservation` model with three states: "reserved" (default), "used", and "unused". Operators and Administrators can change a reservation's status from the detail view. The status is displayed in reservation list views and PDF exports, with filtering by status. All labels are displayed in Spanish using the existing Django i18n system.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: Django 5.0.x, psycopg2-binary, WeasyPrint 62.0

**Storage**: PostgreSQL 16

**Testing**: pytest 9.1.x + pytest-django 4.12.x

**Target Platform**: Linux (Docker/Gunicorn container)

**Project Type**: Web application (Django monolith with multiple apps)

**Performance Goals**: Standard web app — status changes and list views should respond in under 2 seconds for typical gym data volumes

**Constraints**: TDD mandatory (Red-Green-Refactor). Spanish i18n required for all UI labels. Integration tests required for contract changes.

**Scale/Scope**: Small gym operation — <100 reservations/day, <1000 active clients

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Evaluation

| Principle | Status | Justification |
|-----------|--------|---------------|
| I. Code Quality | ✅ PASS | YAGNI applied: only adding a single enum-style status field. No dead code or unresolved TODOs will be committed. |
| II. Testing Standards (NON-NEGOTIABLE) | ✅ PASS | TDD will be followed: tests written first, then implementation. Integration tests required for view-level changes (reservation list, detail, PDF, filter). Existing tests in `test_reservations_list.py` will be updated. |
| III. User Experience Consistency | ✅ PASS | Status labels will use Django i18n with existing Spanish locale (`es`). Error messages will follow existing patterns. |
| IV. Performance Requirements | ✅ PASS | Feature has minimal performance impact — a single status field addition. Existing response time expectations (<2s) are maintained. |
| Development Workflow | ✅ PASS | Follows Specify → Plan → Tasks → Implement cycle. Feature branch uses sequential numbering (013). |

**Result**: GATE PASSED — no violations to justify in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/013-reservation-status/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── models.py              # +status field (CharField with choices)
│       ├── views.py               # +status update logic in detail view
│       ├── forms.py               # +status field in form (if applicable)
│       ├── urls.py                # +status change URL pattern
│       ├── admin.py               # +status in list display
│       ├── templates/
│       │   └── reservations/
│       │       ├── reservation_list.html       # +status column
│       │       ├── reservation_list_by_slot.html # +status column
│       │       ├── reservation_list_pdf.html    # +status column
│       │       ├── reservation_detail.html      # +status display + action buttons
│       │       └── reservation_form.html        # (no changes needed)
│       ├── templatetags/
│       │   └── reservation_extras.py            # (no changes needed)
│       └── migrations/
│           └── 0003_reservation_status.py       # New migration
├── locale/
│   └── es/
│       └── LC_MESSAGES/
│           └── django.po          # +status labels translations
└── tests/
    └── test_reservations_list.py  # +status-related tests
```

**Structure Decision**: The Django app structure remains unchanged. Changes are localized to the `reservations` app with a new migration, modified views/templates, and updated tests. The structure matches the existing monolith pattern used throughout the project.

## Complexity Tracking

> **Not needed** — all Constitutional checks passed without violations.
