# Tasks: Auto-set Date on Class Slot Selection

**Input**: Design documents from `specs/041-auto-date-class-slot/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests included per TDD requirement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root — adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

No setup tasks required — the project is fully initialized with all dependencies installed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

No foundational tasks required — the existing Django app and testing infrastructure are already in place.

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — Auto-Date on Class Slot Select (Priority: P1) 🎯 MVP

**Goal**: When a class slot is selected on the reservation create page, the date field auto-populates based on the day-of-week and time rules.

**Independent Test**: Load `/reservations/create/`, select a class slot, and verify the date input updates to the correct date per the auto-date algorithm.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [P] [US1] Test: auto-date sets date to next week when today matches slot day-of-week and time is before earliest class time in `backend/tests/test_reservations.py`
- [x] T002 [US1] Test: auto-date sets date to this week when slot day-of-week is a future day in `backend/tests/test_reservations.py`
- [x] T003 [US1] Test: auto-date sets date to next week when slot day-of-week is a past day in `backend/tests/test_reservations.py`
- [x] T004 [US1] Test: no date change when no class slot is selected in `backend/tests/test_reservations.py`

### Implementation for User Story 1

- [x] T005 [US1] Create static JS file with auto-date calculation logic in `backend/apps/reservations/static/reservations/js/auto-date.js`
- [x] T006 [US1] Expose active class slots as JSON in view context in `backend/apps/reservations/views.py`
- [x] T007 [US1] Wire auto-date JS into reservation create template in `backend/apps/reservations/templates/reservations/reservation_form.html`

**Checkpoint**: At this point, User Story 1 should be fully functional — date auto-populates on class slot selection

---

## Phase 4: User Story 2 — Edge Cases and Time-Boundaries (Priority: P2)

**Goal**: The auto-date logic correctly handles time boundaries: past/future days, same-day before/after class times, cross-week boundaries.

**Independent Test**: Test all examples from the spec's examples table and verify correct auto-date output for each.

### Tests for User Story 2 ⚠️

- [x] T008 [P] [US2] Test: same-day slot selected when time is past earliest class time → next week in `backend/tests/test_reservations.py`
- [x] T009 [US2] Test: manual date override is preserved when class slot changes in `backend/tests/test_reservations.py`

### Implementation for User Story 2

- [x] T010 [US2] Verify server-side validation matches JS calculation logic in `backend/apps/reservations/views.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T011 Run all tests pass: `docker compose exec web uv run pytest tests/ -v`
- [x] T012 Verify reservation creation works end-to-end with auto-date
- [x] T013 Verify existing reservation tests still pass (no regression)
- [x] T014 Save AI session file in `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — already complete
- **Foundational (Phase 2)**: No dependencies — already complete
- **US1 (Phase 3)**: Can start immediately — foundational auto-date logic
- **US2 (Phase 4)**: Depends on US1 completion (edge cases build on core logic)
- **Polish (Phase 5)**: Depends on all stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — core auto-date implementation
- **User Story 2 (P2)**: Depends on US1 — edge cases extend core logic

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation then makes tests pass
- Story complete before moving to next priority

### Parallel Opportunities

- T001, T002, T003 (US1 tests) can run in parallel
- T005 and T006 (US1 implementation) can run in parallel (different files)
- T008 (US2 test) can start after T005 completes

---

## Parallel Example: User Story 1

```bash
# Launch tests for User Story 1 together:
Task: "T001 - Test same-day before earliest time → next week"
Task: "T002 - Test future day this week → this week"
Task: "T003 - Test past day → next week"

# Launch implementation:
Task: "T005 - Create auto-date.js"
Task: "T006 - Expose class slots JSON in view"
Task: "T007 - Wire JS into template"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 — core auto-date logic
2. **STOP and VALIDATE**: Test US1 independently
3. Deploy/demo if ready

### Environment Reference

- **Run tests**: `docker compose exec web uv run pytest`
- **Run specific test**: `docker compose exec web uv run pytest tests/test_reservations.py -v -k <test_name>`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- No new dependencies, no schema changes — pure JS + template change
