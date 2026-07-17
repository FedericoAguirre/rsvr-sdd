# Implementation Plan: Payments Columns Stripe

**Branch**: `044-payments-columns-stripe` | **Date**: 2026-07-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/044-payments-columns-stripe/spec.md`

## Summary

Reorder the "Reservas asociadas" grid columns on `payments/{id}/` from Date/Equipment/Class Slot/Status to Class Slot/Date/Equipment/Status and add the Bootstrap `table-striped` class for alternating row colors. Single template change in `backend/apps/payments/templates/payments/payment_detail.html`.

## Technical Context

**Language/Version**: Python 3.13, Django 5.0

**Primary Dependencies**: Django templates, Bootstrap 5 (`table-striped` class)

**Storage**: N/A — no data model changes

**Testing**: pytest + Django TestCase via `docker compose exec web uv run pytest`

**Target Platform**: Linux server (Docker), modern browsers

**Project Type**: Web application (Django)

**Performance Goals**: N/A — trivial template change, no measurable performance impact

**Constraints**: Must maintain existing i18n and functionality; no new strings needed (all column headers already translated)

**Scale/Scope**: Single template file, 2 test cases

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| TDD (Tests before implementation) | ✅ PASS | Tests will be written and reviewed before template change |
| i18n — no raw user-visible strings | ✅ PASS | No new strings introduced; existing trans tags reused |
| YAGNI — no unnecessary complexity | ✅ PASS | Single template change, no new models/views/logic |
| Code quality — linting, no dead code | ✅ PASS | Only modifying existing template tags |
| AI session file required before PR | ✅ PASS | Will be saved before merge |

**No violations to justify** — Complexity Tracking section omitted.

## Project Structure

### Documentation (this feature)

```text
specs/044-payments-columns-stripe/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       └── templates/
│           └── payments/
│               └── payment_detail.html   # Single file to modify
└── tests/
    └── test_payments_detail.py           # New test file for column order
```

**Structure Decision**: Django web app with apps inside `backend/apps/`. Tests mirror the app structure under `backend/tests/`.

## Complexity Tracking

*No constitution violations to justify — Complexity Tracking section omitted.*
