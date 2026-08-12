# Implementation Plan: Batch Payment-Day Reservations

**Branch**: `064-batch-payment-reservation` | **Date**: 2026-08-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/064-batch-payment-reservation/spec.md`

## Summary

Change the existing payment batch-reservation window so it begins on the payment date when a class slot on that date has not started. If all payment-day slots have started, begin on the next date with eligible availability. The window ends 20 calendar days after its first eligible date. Preserve the existing class-count, maximum-20, availability, capacity, weekday mapping, conflict, and partial-failure rules.

The date-window calculation will be centralized and shared by the batch-data response and batch-create validation so the modal cannot display a range that the server rejects.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Django 5.0.x, pytest 9.1.x, pytest-django 4.12.x, existing Bootstrap 5.3 browser UI

**Storage**: Existing SQLite development database and PostgreSQL deployment database; no schema change expected

**Testing**: pytest with pytest-django; Django request tests and form validation tests in `backend/tests/test_payments_batch.py`

**Target Platform**: Server-rendered web application in desktop and mobile browsers

**Project Type**: Django web application with server-rendered templates and JSON endpoints

**Performance Goals**: Batch date data and validation remain within the specified 2-second response target for at least 95% of normal attempts

**Constraints**: Use the configured `America/Denver` business time zone; preserve existing batch rules and partial-conflict behavior; all new user-visible text must use i18n

**Scale/Scope**: One payment batch at a time, with 1–20 requested reservations and a 20-calendar-day selection window; no new persistence or external integration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Code Quality**: PASS. The design centralizes duplicated date-window logic and avoids new abstractions beyond the feature boundary.
- **II. Testing Standards**: PASS with implementation gate. Tests must be added first and fail before the production change; request-level coverage is required for the JSON endpoint and batch creation validation.
- **III. UX Consistency and i18n**: PASS. Existing modal interaction and Spanish translations remain; any new validation text must use Django translations.
- **IV. Performance**: PASS. The 2-second/95% requirement is recorded in the spec and technical context; the plan avoids per-date unbounded queries by reusing bounded date-window queries.
- **V. External Documentation**: PASS for planning. No new dependency or library API is introduced. Any implementation using Django or pytest APIs must follow the repository's required Context7 lookup before code is written.
- **Development workflow**: PASS. The work remains on the numbered feature branch and follows Specify → Plan → Tasks → Implement.

## Project Structure

### Documentation (this feature)

```text
specs/064-batch-payment-reservation/
├── plan.md              # This plan
├── research.md          # Phase 0 decisions
├── data-model.md        # Phase 1 domain and validation model
├── quickstart.md        # Phase 1 validation guide
├── contracts/
│   └── batch-reservation.md  # Existing JSON endpoint contracts
└── tasks.md             # Phase 2 output from /speckit.tasks
```

### Source Code (repository root)

```text
backend/
├── apps/payments/
│   ├── batch_reservations.py       # Shared reservation-window calculation
│   ├── forms.py                    # Batch date validation uses shared window
│   ├── views.py                    # Batch data endpoint uses shared window
│   └── templates/payments/
│       └── payment_detail.html     # Existing date-grid behavior consumes window
└── tests/
    └── test_payments_batch.py      # Boundary, regression, and contract tests
```

**Structure Decision**: Keep the existing Django payments app and payment-detail modal. Add one small domain helper module to remove the duplicated window algorithm, update the form and JSON view to call it, and extend the existing batch test module. No model, migration, URL, or external API changes are required.

## Complexity Tracking

No constitution violations. The helper module is justified because the same date-window rule currently exists independently in `BatchDataView` and `BatchReservationForm`; keeping two copies would allow the UI and server validation to diverge.
