# Implementation Plan: Restore 20-Day Batch Reservation Window

**Branch**: `066-fix-batch-window` | **Date**: 2026-08-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/066-fix-batch-window/spec.md`

## Summary

Extend the shared batch reservation window until it contains 20 Monday-through-Friday calendar dates, rather than ending 20 calendar days after the start and exposing only 15 weekday buttons. Keep the existing start-date selection, same-day cutoff, class-slot validation, endpoint field names, and weekday-aligned modal rendering unchanged. Add regression tests for Monday and midweek starts, month boundaries, and the reported payment scenario.

## Technical Context

**Language/Version**: Python 3.12; browser JavaScript already used by the payment modal

**Primary Dependencies**: Django 5.0, pytest/pytest-django, existing Bootstrap 5.3 modal and i18n presentation

**Storage**: PostgreSQL through existing Django `Payment`, `Reservation`, and `ClassSlot` models; no schema changes

**Testing**: `uv run pytest` from `backend/`; focused payment batch tests; targeted Ruff checks for changed Python files

**Target Platform**: Existing Django web application and deployed payment modal

**Project Type**: Server-rendered Django web application with browser-side date-grid rendering

**Performance Goals**: Calculate the end date with a bounded loop over at most 28 calendar days for a five-day weekday schedule; preserve the existing single batch-data request and normal modal response time

**Constraints**: No new dependency, migration, or endpoint field; preserve the existing start date and validation rules; weekends are not selectable dates in the modal; use the configured business timezone for the start-date cutoff

**Scale/Scope**: One payment batch window with a target of 20 selectable weekdays and the existing class-slot/date validation rules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code quality**: PASS. A small date-count helper replaces the incorrect fixed offset; no dead code or unresolved TODOs are planned.
- **Testing/TDD**: PASS with review gate. Add failing window-boundary tests before changing the helper and retain all existing batch regressions.
- **UX consistency/i18n**: PASS. The modal structure, translated labels, weekday alignment, error messages, and endpoint response shape remain unchanged.
- **Performance**: PASS. The calculation is a bounded in-memory date loop and adds no database query or network request.
- **Documentation**: PASS. Update batch reservation operator documentation and quickstart scenarios to state that 20 means selectable weekdays.
- **Dependency integrity**: PASS. No new library or framework API is introduced.
- **Security and authorization**: PASS. Existing authenticated views and form validation remain unchanged.
- **Complexity**: PASS. Counting eligible weekdays is the smallest correction for the observed 15-versus-20 discrepancy.

## Project Structure

### Documentation (this feature)

```text
specs/066-fix-batch-window/
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
backend/apps/payments/batch_reservations.py
backend/apps/payments/views.py
backend/apps/payments/forms.py
backend/apps/payments/templates/payments/payment_detail.html
backend/tests/test_payments_batch.py
docs/batch_reservations.md
```

**Structure Decision**: Keep the existing payment feature structure. The backend window helper changes its end-date calculation; the view, form, and modal consume the same fields and preserve existing behavior. Tests remain in the existing payment batch test module.

## Phase 0: Research

See [research.md](./research.md). Repository and deployment verification establish that the current `start + 20 calendar days` interval renders 15 weekdays when weekends are omitted.

## Phase 1: Design

- See [data-model.md](./data-model.md) for the window's target count and inclusive end-date rules.
- See [contracts/batch-reservation.md](./contracts/batch-reservation.md) for the unchanged response and submission contract.
- See [quickstart.md](./quickstart.md) for focused, full-suite, and deployment verification.

## Complexity Tracking

| Addition | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|---------------------------------------|
| Inclusive weekday counter for the window end | A fixed 20-calendar-day offset produces only 15 selectable weekdays | Increasing the offset by an arbitrary constant fails for non-weekday starts and does not express the business requirement |
