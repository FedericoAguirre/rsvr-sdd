# Implementation Plan: Batch Reservation Date Alignment

**Branch**: `065-batch-reservation-date-alignment` | **Date**: 2026-08-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/065-batch-reservation-date-alignment/spec.md`

## Summary

Correct the batch reservation modal's weekday grid so dates are positioned by their actual calendar weekday instead of being chunked into rows from the first available date. Preserve the existing payment-day window calculation, date validation, endpoint payload, reservation creation, and translations. The frontend will group dates by calendar week, render weekday-position placeholders for dates before the range start, and retain each date's ISO value unchanged when selected.

## Technical Context

**Language/Version**: Python 3.12; browser JavaScript supported by the existing application

**Primary Dependencies**: Django 5.0, Bootstrap 5.3, pytest/pytest-django, existing i18n translation system

**Storage**: PostgreSQL via existing Django models; no schema changes

**Testing**: `uv run pytest` from `backend/`; focused batch reservation tests; static/template regression assertions for weekday-grid behavior; Ruff targeted checks (`E,F,I`)

**Target Platform**: Django web application on POSIX-compatible host/container; desktop and mobile browsers supported by the existing modal

**Project Type**: Server-rendered Django web application with progressively enhanced browser JavaScript

**Performance Goals**: Render the existing 20-day maximum batch period without additional network requests; preserve current modal load behavior and response shape

**Constraints**: No database migration, no new dependency, no change to the public batch endpoint contract, all user-visible text remains translated, and selected ISO dates must be submitted unchanged

**Scale/Scope**: One payment batch modal displaying at most the existing 20-day reservation window and five weekday columns per calendar week

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code quality**: PASS. The change is limited to the existing payment modal rendering and regression tests; no dead code or unresolved TODOs are planned.
- **Testing/TDD**: PASS with required review gate. Add failing regression coverage for a range beginning Tuesday or later before changing the grid renderer; retain existing batch tests and run the full suite.
- **UX consistency/i18n**: PASS. Reuse existing translated weekday labels, Bootstrap classes, modal behavior, and validation messages. No new user-visible strings are required.
- **Performance**: PASS. Use in-memory grouping of the already loaded date range; no additional queries or requests. Validate the existing 20-day scope remains responsive.
- **Documentation**: PASS. Update the feature quickstart and operator-facing batch reservation documentation if behavior wording changes.
- **Dependency integrity**: PASS. No new dependency or library API is introduced; existing Django, Bootstrap, and browser APIs are used in their current code paths.
- **Complexity**: PASS. A small date-grid grouping helper is justified because sequential slicing cannot preserve weekday columns when the range starts midweek.

## Project Structure

### Documentation (this feature)

```text
specs/065-batch-reservation-date-alignment/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── batch-reservation.md
└── tasks.md              # Created by /speckit.tasks
```

### Source Code

```text
backend/apps/payments/templates/payments/payment_detail.html  # Date-grid rendering and weekday placement
backend/apps/payments/templates/payments/_batch_modal.html    # Existing modal shell; unchanged unless accessibility fixes are needed
backend/apps/payments/views.py                                # Existing batch-data contract; preserved
backend/apps/payments/forms.py                                # Existing exact-date validation; preserved
backend/tests/test_payments_batch.py                          # Backend contract and regression coverage
backend/tests/test_payment_detail_template.py                 # New focused static/template alignment coverage if required by test layout
docs/batch_reservations.md                                    # Existing operator documentation
```

**Structure Decision**: Keep the existing Django payment feature structure. The date alignment is a presentation-layer correction in `payment_detail.html`; backend calculations and the JSON contract remain authoritative and unchanged unless tests demonstrate a required contract adjustment.

## Phase 0: Research

See [research.md](./research.md). Repository research confirms the current defect is caused by rendering filtered dates in five-item slices rather than calendar-week buckets. No unresolved technical unknowns remain.

## Phase 1: Design

- See [data-model.md](./data-model.md) for the date-grid view model and unchanged domain entities.
- See [contracts/batch-reservation.md](./contracts/batch-reservation.md) for the preserved batch-data and batch-create interfaces.
- See [quickstart.md](./quickstart.md) for focused and full validation commands.

## Complexity Tracking

| Addition | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|---------------------------------------|
| Calendar-week grouping with weekday placeholders | A range beginning midweek must retain its actual weekday column | Sequentially slicing dates into groups of five causes Tuesday-start dates to render under Monday |
