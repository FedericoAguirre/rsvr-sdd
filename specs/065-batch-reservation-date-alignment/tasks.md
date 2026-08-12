---

description: "Implementation tasks for batch reservation date alignment"

---

# Tasks: Batch Reservation Date Alignment

**Input**: Design documents from `/specs/065-batch-reservation-date-alignment/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Testing**: Required by the project constitution. Tests must be written first and fail before the related implementation task.

## Phase 1: Setup

**Purpose**: Confirm the existing payment modal and test baseline before changing behavior.

- [X] T001 Run the focused baseline suite for `backend/tests/test_payments_batch.py` and record the current result before implementation (`18 passed`).
- [X] T002 [P] Review the existing date-grid code in `backend/apps/payments/templates/payments/payment_detail.html` against `specs/065-batch-reservation-date-alignment/data-model.md` and identify the exact sequential-slicing path to replace.

---

## Phase 2: Foundational

**Purpose**: Establish shared regression coverage and contract boundaries before user-story implementation.

- [X] T003 [P] Add date-grid regression helpers in `backend/tests/test_payment_detail_template.py` that load the payment detail template source and assert calendar-week rendering markers.
- [X] T004 [P] Add a batch-data contract regression in `backend/tests/test_payments_batch.py` confirming `date_range`, `reserved_dates`, and `class_slots` remain unchanged for the alignment feature.

**Checkpoint**: Baseline and contract tests are ready; user-story implementation can begin.

---

## Phase 3: User Story 1 - Select Aligned Batch Dates (Priority: P1) 🎯 MVP

**Goal**: Render every date beneath the weekday column matching its actual calendar weekday, including ranges that begin midweek.

**Independent Test**: Run the template alignment tests with date ranges beginning Tuesday, Wednesday, Thursday, and Friday; confirm leading empty cells and exact weekday positions.

### Tests for User Story 1

> Write these tests first and verify they fail against the current sequential five-item renderer.

- [X] T005 [US1] Add failing alignment assertions in `backend/tests/test_payment_detail_template.py` for midweek starts, calendar-week boundaries, and leading weekday placeholders.
- [X] T006 [P] [US1] Add a failing exact-date assertion in `backend/tests/test_payment_detail_template.py` confirming each rendered date button retains its original `data-date` ISO value.

### Implementation for User Story 1

- [X] T007 [US1] Replace sequential five-date slicing with Monday-based calendar-week grouping in `backend/apps/payments/templates/payments/payment_detail.html`, placing each weekday date at its `isoDow` column and rendering empty leading cells.
- [X] T008 [US1] Preserve translated weekday headers, reserved-date filtering, button selection behavior, and `selectedDates` payload values in `backend/apps/payments/templates/payments/payment_detail.html`.
- [X] T009 [US1] Run `backend/tests/test_payment_detail_template.py` and the focused batch suite, then verify the new alignment tests pass without changing the existing endpoint contract.

**Checkpoint**: The modal displays midweek-starting ranges in correct weekday columns and the selected dates remain exact.

---

## Phase 4: User Story 2 - Choose the Correct Starting Date (Priority: P1)

**Goal**: Preserve and verify the existing starting-date priority while the corrected grid displays the resulting range accurately.

**Independent Test**: Exercise default payment day, selected payment date, and latest-reservation fallback scenarios through the batch-data endpoint and compare the returned start date with the expected candidate.

### Tests for User Story 2

- [X] T010 [US2] Add or strengthen priority-order tests in `backend/tests/test_payments_batch.py` for default payment day, valid selected payment date, and day-after-latest-reservation fallback.

### Implementation for User Story 2

- [X] T011 [US2] Verify `backend/apps/payments/batch_reservations.py` and `backend/apps/payments/views.py` continue to return the correct inclusive `date_range` without introducing weekday normalization or Monday hardcoding.
- [X] T012 [US2] Update `docs/batch_reservations.md` with the corrected midweek-start display behavior and the preserved starting-date priority if the existing documentation does not state it.

**Checkpoint**: The date range starts from the correct business rule candidate and the UI renders that start date in its actual weekday column.

---

## Phase 5: User Story 3 - Preserve Existing Batch Behavior (Priority: P2)

**Goal**: Ensure exact date submission, class-slot validation, duplicate handling, and conflict behavior remain unchanged.

**Independent Test**: Select valid dates from the aligned grid, submit the batch, and run invalid-date scenarios; confirm successful reservations use exact dates and existing errors remain actionable.

### Tests for User Story 3

- [X] T013 [P] [US3] Add or strengthen exact-date batch creation assertions in `backend/tests/test_payments_batch.py` for dates crossing a month boundary and matching class-slot weekdays.
- [X] T014 [P] [US3] Add or strengthen invalid-date, duplicate-date, unavailable-slot, and outside-window assertions in `backend/tests/test_payments_batch.py`.

### Implementation for User Story 3

- [X] T015 [US3] Verify `backend/apps/payments/forms.py` continues validating the submitted ISO dates against the existing window, count, duplicate, cutoff, and class-slot rules without UI-specific assumptions.
- [X] T016 [US3] Verify `backend/apps/payments/views.py` creates reservations using each submitted date unchanged and preserves existing error responses.

**Checkpoint**: All existing batch reservation behavior remains independently testable after the alignment change.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the complete feature, documentation, quality gates, and user-facing behavior.

- [X] T017 [P] Update `specs/065-batch-reservation-date-alignment/quickstart.md` with the final focused test command and browser scenarios if implementation details require clarification.
- [X] T018 Run the complete backend suite from `backend/` with `uv run pytest` and confirm no regressions across payment, reservation, and template tests (`342 passed`).
- [X] T019 Run targeted Ruff checks for changed feature files in `backend/apps/payments/templates/payments/payment_detail.html` and `backend/tests/test_payment_detail_template.py`; confirm the new test file passes targeted checks while unrelated baseline findings remain documented.
- [X] T020 Validate the weekday-alignment scenarios from `specs/065-batch-reservation-date-alignment/quickstart.md` through the template regression suite, including midweek starts and exact date preservation; browser execution remains a manual follow-up because no browser service is available in the environment.
- [X] T021 Verify `backend/apps/payments/templates/payments/payment_detail.html` contains no new untranslated user-visible strings and that existing Spanish weekday labels still render.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes the baseline.
- **Foundational (Phase 2)**: Depends on T001 and T002; creates regression boundaries before implementation.
- **User Story 1 (Phase 3)**: Depends on Phase 2; delivers the MVP alignment correction.
- **User Story 2 (Phase 4)**: Depends on Phase 2 and can run alongside US1 after the shared contract tests exist.
- **User Story 3 (Phase 5)**: Depends on Phase 2 and can run alongside US1 and US2 because it preserves existing backend behavior.
- **Polish (Phase 6)**: Depends on all selected user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on other stories after Phase 2; MVP.
- **User Story 2 (P1)**: No dependency on US1; verifies the existing backend range calculation independently.
- **User Story 3 (P2)**: No dependency on US1 or US2; verifies existing submission and validation behavior independently.

### Within Each User Story

- Tests MUST be written and fail before implementation changes.
- Rendering or backend behavior changes follow the failing regression tests.
- Focused story tests must pass before cross-cutting validation.

## Parallel Opportunities

- T003 and T004 can run in parallel after the baseline review.
- T005 and T006 can run in parallel because they extend the same test fixture with independent assertions.
- T010, T013, and T014 can be prepared in parallel after the foundational contract review.
- US1, US2, and US3 can be implemented in parallel after Phase 2, provided test files are coordinated to avoid conflicting edits.
- T017 and T021 can run in parallel during polish.

## Parallel Example: User Story 1

```text
Task: Add failing midweek and leading-placeholder assertions in backend/tests/test_payment_detail_template.py
Task: Add failing exact data-date preservation assertions in backend/tests/test_payment_detail_template.py
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 baseline and Phase 2 regression boundaries.
2. Complete User Story 1, including failing tests, calendar-week grouping, and focused validation.
3. Stop and manually validate a Tuesday-start range in the modal.
4. Deliver the alignment correction as the MVP if the existing backend behavior remains green.

### Incremental Delivery

1. Add User Story 2 regression coverage to protect the existing starting-date priority.
2. Add User Story 3 coverage to protect exact submission and validation behavior.
3. Run the full suite, targeted lint, documentation, and manual browser checks.

## Notes

- Every task uses the required checkbox, sequential ID, optional `[P]` marker, required story label for story tasks, and an exact repository file path.
- No migrations, new dependencies, endpoint changes, or translation keys are expected.
- Stop at each checkpoint to review test results before proceeding.
