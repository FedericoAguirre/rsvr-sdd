# Tasks: Filter State Saving

**Input**: Design documents from `/specs/001-filter-state-saving/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md

**Tests**: Included per constitution mandate (TDD is non-negotiable). Tests MUST be written first and MUST fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- Paths below assume Django web app structure from plan.md

---

## Phase 1: Setup

**Purpose**: Verify development environment and confirm the existing test baseline

- [x] T001 Confirm Docker environment is running (`docker-compose ps`) and tests pass for `tests/test_reservations_list.py`

**Checkpoint**: Environment ready

---

## Phase 2: User Story 1 - Preserve Filter State After Postback (Priority: P1) 🎯 MVP

**Goal**: Reservation filter form fields (class_slot, date, status) retain their selected values across all postback operations.

**Independent Test**: Apply all three filters (class_slot, date, status), submit the form, then assert the rendered HTML contains `selected` on the matching class_slot `<option>`, the correct `value` on the date `<input>`, and `selected` on the matching status `<option>`.

### Tests for User Story 1 (TDD — write first, ensure FAIL before implementation) ⚠️

- [x] T002 [US1] Write failing test for class_slot dropdown preserving selected value after filter submission in `backend/tests/test_reservations_list.py`

### Implementation for User Story 1

- [x] T003 [US1] Add `selected` attribute to class_slot `<option>` matching `class_slot.pk` in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [x] T004 [US1] Verify date input preserves `request.GET.date` value across postbacks (already works — confirmed by test) in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [x] T005 [US1] Verify status filter dropdown preserves `selected` state for both populated and empty filter values (already works — confirmed by test) in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [x] T006 [US1] Run test — confirm all filter state tests pass

**Checkpoint**: Filter state is preserved after postback — User Story 1 independently testable

---

## Phase 3: User Story 2 - Clear Filters (Priority: P2)

**Goal**: Users can reset all active filters to their default state with a single action.

**Independent Test**: Apply filter values, click "Clear Filters", and confirm the reservations list shows the full unfiltered dataset with all filter fields in their default state.

### Tests for User Story 2 (TDD — write first, ensure FAIL before implementation) ⚠️

- [x] T007 [US2] Write test for "Clear Filters" — confirmed no selected options when no GET params in `backend/tests/test_reservations_list.py`

### Implementation for User Story 2

- [x] T008 [US2] Add "Clear Filters" link targeting `reservations:reservation-list` in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [x] T009 [US2] Ensure view renders empty/default filter state when no GET params provided (already works — verified by tests)
- [x] T010 [US2] Run test — confirm all 6 filter state tests pass

**Checkpoint**: Clear Filters action works — User Story 2 independently testable

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup, documentation, and final validation

- [x] T011 [P] Move source feature file from `ai/features/todos/02b_filter_state_saving.md` to `ai/features/done/02b_filter_state_saving.md` (per constitution workflow)
- [x] T012 [P] Run full test suite — 61/61 passed, zero regressions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion
- **User Story 2 (Phase 3)**: Depends on Setup completion — no dependencies on US1 (independently testable)
- **Polish (Phase 4)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup — no dependencies on other stories
- **User Story 2 (P2)**: Can start after Setup — independently testable, no dependency on US1

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation tasks must be completed in order
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004, T005 can run in parallel (modifying different parts of the same template — use caution with concurrent edits to same file)
- T011, T012 can run in parallel (different files/operations)

---

## Parallel Example: User Story 1

```bash
# Task: Verify date input preserves value in backend/apps/reservations/templates/reservations/reservation_list.html
# Task: Verify status filter preserves value in backend/apps/reservations/templates/reservations/reservation_list.html
```
Note: These touch the same file — best done sequentially by a single developer.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: User Story 1
3. **STOP and VALIDATE**: Test filter state preservation independently
4. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup → Environment ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Bug Fix Approach

This is a targeted bug fix in existing code. The primary change is a single template modification (`reservation_list.html`) to add the `selected` attribute to the class_slot dropdown. No new models, services, or endpoints required.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Primary fix is in `reservation_list.html` template — class_slot dropdown lacks `selected` attribute
