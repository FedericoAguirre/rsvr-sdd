# Tasks: Batch Payment-Day Reservations

**Input**: Design documents from `specs/064-batch-payment-reservation/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Included because the project constitution requires test-first development and the feature changes existing reservation boundaries.

## Phase 1: Setup

**Purpose**: Establish the baseline before changing the shared batch-reservation rule.

- [X] T001 Run `uv run pytest backend/tests/test_payments_batch.py` and record the baseline result in `specs/064-batch-payment-reservation/quickstart.md`

---

## Phase 2: Foundational

**Purpose**: Confirm the shared boundary contract before story implementation.

- [X] T002 [P] Add the derived-window examples and payment timestamp assumptions to `specs/064-batch-payment-reservation/data-model.md`
- [X] T003 [P] Add request/response assertions for the unchanged batch endpoint fields to `backend/tests/test_payments_batch.py`

**Checkpoint**: Shared endpoint shape and baseline expectations are documented before user-story implementation.

---

## Phase 3: User Story 1 - Reserve eligible classes on payment day (Priority: P1) 🎯 MVP

**Goal**: Include still-upcoming classes on the payment date and expose the correct 20-calendar-day window in the existing batch modal.

**Independent Test**: Create five-class payments with controlled creation timestamps at 17:00, 19:00, 19:20, and 20:20 on August 11, 2026; verify the returned `date_range` and eligible payment-day dates match the four acceptance scenarios.

### Tests for User Story 1

> **Write these tests first and verify they fail before implementation.**

- [X] T004 [US1] Add 17:00 and 19:00 payment-day inclusion tests for `GET /payments/{id}/batch-data/` in `backend/tests/test_payments_batch.py`
- [X] T005 [US1] Add 19:20 cutoff and 20:20 next-date-start tests for `GET /payments/{id}/batch-data/` in `backend/tests/test_payments_batch.py`
- [X] T006 [US1] Add batch-create validation tests proving a payment-day date is accepted only when its class start time is later than `Payment.created_at` in `backend/tests/test_payments_batch.py`

### Implementation for User Story 1

- [X] T007 [US1] Implement the shared payment-day reservation-window calculation using `Payment.date`, localized `Payment.created_at`, active class slots, and the client's latest reservation in `backend/apps/payments/batch_reservations.py`
- [X] T008 [US1] Update `BatchDataView` to return the shared window's first eligible date and 20-calendar-day end date in `backend/apps/payments/views.py`
- [X] T009 [US1] Update `BatchReservationForm.clean_dates` to validate selected dates against the shared window in `backend/apps/payments/forms.py`
- [X] T010 [US1] Verify the existing date-grid JavaScript consumes the new `date_range` without reintroducing the next-Monday rule in `backend/apps/payments/templates/payments/payment_detail.html`

**Checkpoint**: User Story 1 is independently functional when all four timing scenarios pass through the endpoint, modal, and batch-create validation.

---

## Phase 4: User Story 2 - Preserve batch reservation rules (Priority: P2)

**Goal**: Retain existing count, capacity, weekday, availability, conflict, and partial-failure behavior while changing only the reservation-window start boundary.

**Independent Test**: Run the existing batch regression suite plus new cases for latest client reservations, inactive slots, exact class count, maximum 20 reservations, weekday mapping, and conflicts; verify no invalid reservation is accepted.

### Tests for User Story 2

> **Write these tests first and verify they fail before implementation.**

- [X] T011 [US2] Add regression tests for latest-client-reservation offset and next-active-slot fallback in `backend/tests/test_payments_batch.py`
- [X] T012 [US2] Add regression assertions for exact count, maximum 20, duplicate dates, weekday mapping, and out-of-window rejection in `backend/tests/test_payments_batch.py`
- [X] T013 [US2] Add regression assertions for equipment/class-slot availability and partial conflict responses in `backend/tests/test_payments_batch.py`

### Implementation for User Story 2

- [X] T014 [US2] Preserve existing quantity, duplicate-date, maximum-count, weekday, and active-slot validation while routing all date-range checks through `backend/apps/payments/forms.py`
- [X] T015 [US2] Preserve existing partial-success and payment-association behavior while applying the shared window during `backend/apps/payments/views.py` batch creation

**Checkpoint**: User Stories 1 and 2 pass independently, with no regression in existing batch reservation rules.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Complete verification, documentation, and maintainability checks.

- [X] T016 [P] Add the operator-facing payment-day batch reservation workflow and boundary examples to `docs/batch_reservations.md`
- [X] T017 [P] Review changed payment templates and validation messages for i18n compliance in `backend/apps/payments/templates/payments/payment_detail.html` and `backend/apps/payments/forms.py`
- [X] T018 Run `uv run ruff check backend/apps/payments backend/tests/test_payments_batch.py` and resolve findings in the affected files
- [X] T019 Run `uv run pytest` and verify the complete suite passes in `backend/tests/`
- [X] T020 Run the scenarios in `specs/064-batch-payment-reservation/quickstart.md` and record any deviations in that file

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes the baseline.
- **Foundational (Phase 2)**: Depends on T001; documents the shared contract before implementation.
- **User Story 1 (Phase 3)**: Depends on Phase 2; delivers the MVP.
- **User Story 2 (Phase 4)**: Depends on T007–T009 from User Story 1 because its regression checks validate the shared implementation.
- **Polish (Phase 5)**: Depends on both user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can begin after Phase 2; no dependency on User Story 2.
- **User Story 2 (P2)**: Extends the shared calculation delivered by User Story 1 and must follow it.

### Within Each User Story

- Tests MUST be written and verified failing before implementation tasks.
- Shared calculation precedes endpoint and form integration.
- Endpoint and form integration must both pass before browser validation.
- Each story checkpoint must pass before moving to the next phase.

## Parallel Opportunities

- T002 and T003 can run in parallel after T001.
- T004, T005, and T006 should run sequentially because they modify the same test module.
- T011, T012, and T013 should run sequentially because they modify the same test module.
- T016 and T017 can run in parallel because they affect separate files.

## Parallel Example: User Story 1

```text
Task T004: Add 17:00 and 19:00 inclusion tests in backend/tests/test_payments_batch.py
Task T005: Add 19:20 and 20:20 boundary tests in backend/tests/test_payments_batch.py
Task T006: Add batch-create cutoff validation tests in backend/tests/test_payments_batch.py
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001–T003 baseline and contract setup.
2. Write and fail T004–T006.
3. Implement T007–T010.
4. Run the four boundary scenarios and focused tests.
5. Stop for review/demo before adding regression hardening.

### Incremental Delivery

1. Deliver User Story 1 with the shared window and four payment-time scenarios.
2. Add User Story 2 regression coverage without changing the existing reservation contract.
3. Complete polish, lint, full test, and quickstart validation.

### Environment Reference

- **Install/sync dependencies**: `uv sync`
- **Run focused tests**: `uv run pytest backend/tests/test_payments_batch.py`
- **Run all tests**: `uv run pytest`
- **Run lint**: `uv run ruff check backend/apps/payments backend/tests/test_payments_batch.py`

## Notes

- `[P]` marks tasks that can be performed in parallel without depending on incomplete work.
- Every task includes a sequential ID and an exact repository path.
- No model, migration, URL, or external dependency task is required by the plan.
