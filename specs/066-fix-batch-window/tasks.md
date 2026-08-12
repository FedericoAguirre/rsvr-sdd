---

description: "Implementation tasks for restoring the 20-weekday batch reservation window"

---

# Tasks: Restore 20-Day Batch Reservation Window

**Input**: Design documents from `/specs/066-fix-batch-window/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Testing**: Required by the project constitution. Tests must be written first and fail before the related implementation change.

## Phase 1: Setup

**Purpose**: Establish the baseline and confirm the reported deployment scenario.

- [X] T001 Run the focused baseline suite for `backend/tests/test_payments_batch.py` and record the existing 20-calendar-day expectations before implementation (`19 passed`).
- [X] T002 [P] Verify payment `CASH20260811AC003` and its current batch-data window against `specs/066-fix-batch-window/quickstart.md` without modifying deployment data (`2026-08-31` through `2026-09-20`, 15 weekdays).

---

## Phase 2: Foundational

**Purpose**: Establish shared weekday-count behavior and preserve the existing response contract before user-story changes.

- [X] T003 [P] Add a focused window-end helper test in `backend/tests/test_payments_batch.py` covering inclusive weekday counting, weekend skipping, and month-boundary progression.
- [X] T004 [P] Add a batch-data contract assertion in `backend/tests/test_payments_batch.py` confirming only `date_range.end` semantics change while response field names remain unchanged.

**Checkpoint**: Red regression tests define the 20-weekday behavior and the unchanged endpoint contract.

---

## Phase 3: User Story 1 - Show the Full 20-Day Selection Window (Priority: P1) 🎯 MVP

**Goal**: Extend the server-provided date interval until the modal contains 20 selectable weekdays.

**Independent Test**: Request batch data for Monday-start and midweek-start scenarios and count Monday-through-Friday dates from `date_range.start` through `date_range.end`; each scenario must contain exactly 20 weekdays.

### Tests for User Story 1

> Write these tests first and verify they fail against the current `start + 20 calendar days` implementation.

- [X] T005 [US1] Add failing Monday-start and Tuesday-through-Friday-start date-range assertions in `backend/tests/test_payments_batch.py` for exactly 20 weekdays.
- [X] T006 [P] [US1] Add a failing reported-payment regression in `backend/tests/test_payments_batch.py` asserting that the August 31, 2026 start reaches September 25, 2026 for 20 weekdays.

### Implementation for User Story 1

- [X] T007 [US1] Replace the fixed `timedelta(days=20)` end-date calculation with an inclusive Monday-through-Friday counter in `backend/apps/payments/batch_reservations.py`.
- [X] T008 [US1] Preserve `date_range.start`, `same_day_cutoff`, reserved-date filtering, and class-slot payload fields in `backend/apps/payments/views.py` while returning the extended end date.
- [X] T009 [US1] Verify the existing weekday-column renderer in `backend/apps/payments/templates/payments/payment_detail.html` displays all dates through the extended end date without changing date alignment or selected ISO values.
- [X] T010 [US1] Run the focused batch tests in `backend/tests/test_payments_batch.py` and confirm the new 20-weekday assertions pass while the existing start-date tests remain valid (`21 passed`).

**Checkpoint**: The modal receives an interval containing 20 selectable weekdays, including for the reported payment scenario.

---

## Phase 4: User Story 2 - Preserve Start-Date and Reservation Rules (Priority: P1)

**Goal**: Ensure extending the end date does not alter payment-day cutoff, latest-reservation, exact-date, or invalid-selection behavior.

**Independent Test**: Run the existing payment-day, latest-reservation, duplicate-date, unavailable-slot, and outside-window scenarios and compare their starts and rejection outcomes with the baseline.

### Tests for User Story 2

- [X] T011 [P] [US2] Add or strengthen payment-day cutoff and latest-reservation assertions in `backend/tests/test_payments_batch.py` to verify the start date is unchanged while the end date expands.
- [X] T012 [P] [US2] Add or strengthen exact-date and invalid-selection assertions in `backend/tests/test_payments_batch.py` for duplicate dates, unavailable slots, outside-window dates, and month-boundary dates.

### Implementation for User Story 2

- [X] T013 [US2] Verify `backend/apps/payments/forms.py` validates dates against the extended inclusive window while preserving count, duplicate, cutoff, class-slot, and actionable error rules.
- [X] T014 [US2] Verify `backend/apps/payments/views.py` creates reservations for submitted dates unchanged and retains existing conflict and permission behavior.
- [X] T015 [US2] Update `docs/batch_reservations.md` to document that the batch window contains 20 selectable weekdays and that weekends do not reduce the business count.

**Checkpoint**: Existing reservation rules and start-date behavior are unchanged, with only the available weekday horizon extended.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate the feature against the specification, deployment scenario, documentation, and quality gates.

- [X] T016 [P] Update `specs/066-fix-batch-window/quickstart.md` with final focused commands and the verified reported-payment expected end date.
- [X] T017 Run the complete backend suite from `backend/` with `uv run pytest` and confirm no regressions across payments, reservations, and modal tests (`344 passed`).
- [X] T018 Run targeted Ruff checks for changed Python files with `uv run ruff check apps/payments/batch_reservations.py tests/test_payments_batch.py --select E,F,I` (passed).
- [X] T019 Recheck payment `CASH20260811AC003` in the deployment and confirm the modal provides 20 selectable weekdays without changing stored payment or reservation data (`2026-08-31` through `2026-09-25`, 20 weekdays, 5 associated reservations).
- [X] T020 Scan `backend/apps/payments/templates/payments/payment_detail.html` and `docs/batch_reservations.md` for new untranslated user-visible strings and verify the existing Spanish weekday labels remain intact (passed).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes baseline and deployment evidence.
- **Foundational (Phase 2)**: Depends on Setup and blocks user-story implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational and delivers the MVP window-length correction.
- **User Story 2 (Phase 4)**: Depends on Foundational and can run alongside US1 when test-file changes are coordinated.
- **Polish (Phase 5)**: Depends on both user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on US2 after Phase 2; MVP.
- **User Story 2 (P1)**: No dependency on US1 after Phase 2; protects existing behavior independently.

### Within Each User Story

- Tests MUST be written and fail before the implementation change.
- The shared window helper must be corrected before endpoint and form verification.
- Focused tests must pass before full-suite and deployment validation.

## Parallel Opportunities

- T002, T003, and T004 can run in parallel after the baseline setup.
- T005 and T006 can run in parallel because they add independent boundary scenarios.
- T011 and T012 can run in parallel because they cover separate validation concerns in the same test module and should be coordinated before merging.
- US1 and US2 can be implemented in parallel after Phase 2 if edits to `backend/tests/test_payments_batch.py` are coordinated.
- T016 and T020 can run in parallel during polish.

## Parallel Example: User Story 1

```text
Task: Add failing Monday and midweek 20-weekday range tests in backend/tests/test_payments_batch.py
Task: Add failing CASH20260811AC003 regression in backend/tests/test_payments_batch.py
```

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational phases.
2. Complete User Story 1 with failing tests, inclusive weekday counting, and focused validation.
3. Verify the reported payment reaches 20 selectable weekdays.
4. Stop for review before changing any reservation validation behavior.

### Incremental Delivery

1. Add User Story 2 regression coverage and confirm all existing rules remain intact.
2. Update operator documentation and quickstart verification.
3. Run the full suite, targeted lint, and deployment check.

## Notes

- Every task uses the required checkbox, sequential ID, optional `[P]` marker, story label for user-story tasks, and an exact repository file path.
- No migration, dependency, endpoint shape, or frontend layout change is expected.
- The only intended contract change is the inclusive semantic value of `date_range.end`.
