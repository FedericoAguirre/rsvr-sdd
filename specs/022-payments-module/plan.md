# Implementation Plan: Payments Module

**Branch**: `022-payments-module` | **Date**: 2026-06-24 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/022-payments-module/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command.

## Summary

Replace the current manual spreadsheet-based payment tracking with a digital payments module inside the Django reservation system. Operators can register payments (cash, credit card, debit card, transfer, payments app), view client payment history (paginated, 5 per page), associate payments with reservations (two-step flow on New Reservations page), and soft-delete/edit limited fields. Administrators additionally get access to payment summary reports with Chart.js visualizations grouped by payment type across daily/weekly/monthly/custom date ranges.

## Technical Context

**Language/Version**: Python 3.13, Django 5.0

**Primary Dependencies**: django-chartjs + Chart.js (for report charts), existing Django + HTMX + Bootstrap 5 stack. Image processing for evidence uploads via Django's built-in `ImageField`.

**Storage**: PostgreSQL (production), SQLite (development). Evidence images stored via Django file storage (local filesystem in dev, NEEDS CLARIFICATION: production file storage backend — S3, local persistent volume, or other?).

**Testing**: pytest + pytest-django

**Target Platform**: Linux (Docker) — existing web container

**Project Type**: Web application (Django server-rendered templates + HTMX)

**Performance Goals**: Payment registration under 2 minutes per transaction. Report generation under 3 seconds for any date range. List loading under 1 second for paginated views.

**Constraints**: Must integrate with existing auth system (django.contrib.auth), existing Client model, existing Reservation model, existing ClassSlot model. Must follow existing Django app conventions (backend/apps/). Payment reports require graphs — Chart.js via django-chartjs.

**Scale/Scope**: Moderate volume — 50-200 payments/month. New Django app under `backend/apps/payments/`. Evidence image uploads with 5MB limit, standard web formats.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality (I)**: All new code must pass Ruff linting. No dead code or commented-out code. Complexity additions must be justified in Complexity Tracking.
- **Testing Standards (II — NON-NEGOTIABLE)**: TDD is required. Tests must be written and reviewed by the user first, and must fail before implementation. Integration tests are required for the Payment-Reservation association (inter-module boundary). Unit tests for payment CRUD, payment identifier generation, filtering, and soft-delete behavior.
- **UX Consistency (III)**: All user-facing strings must use Django i18n for Spanish translation. Error messages must be actionable. Consistent with existing module patterns.
- **Performance (IV)**: Measurable criteria defined in success criteria. Structured logging should be added for payment creation and report generation.
- **Development Workflow**: Follow Specify → Plan → Tasks → Implement cycle. Commits must be atomic and descriptive. Session file must be saved in `ai/sessions/` before PR.
- **Governance**: Feature branch name `022-payments-module` follows sequential numbering convention.

**Verdict**: PASS — all gates passable with standard implementation rigor. No constitutional violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/022-payments-module/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/                # New payments Django app
│       ├── models.py            # Payment model
│       ├── views.py             # Payment CRUD + reports views
│       ├── urls.py              # Payment URL routes
│       ├── forms.py             # Payment forms
│       ├── admin.py             # Django admin registration
│       ├── templatetags/
│       │   ├── __init__.py
│       │   └── payment_extras.py  # Template filters/tags
│       ├── templates/
│       │   └── payments/
│       │       ├── payment_list.html        # Client payment history
│       │       ├── payment_form.html        # Create/edit payment
│       │       ├── payment_detail.html      # Payment detail view
│       │       ├── payment_confirm_delete.html # Soft-delete confirmation
│       │       ├── payment_reports.html     # Admin reports view
│       │       └── partials/
│       │           └── payment_row.html     # HTMX row partial
│       └── migrations/
│           └── 0001_initial.py
├── templates/
│   └── base.html                # Updated: add payments nav link
├── config/
│   └── urls.py                  # Updated: include payments URLs
└── tests/
    └── test_payments.py         # Payment tests

specs/022-payments-module/
└── ...
```

**Structure Decision**: Standard Django app following the existing pattern in `backend/apps/`. This matches how `clients`, `equipment`, `classes`, and `reservations` are structured. No additional layers needed for this volume.

## Complexity Tracking

> **No constitution violations detected. Complexity Tracking is not required.**

All complexity is standard Django CRUD with one moderate-complexity feature (payment identifier auto-generation with per-day per-type counters) and one inter-module integration (Payment-Reservation association) — both justified by core functional requirements.
