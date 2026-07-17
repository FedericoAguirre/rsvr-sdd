# Tasks: Update Auto-Date Algorithm

**Input**: Design documents from `/specs/047-update-date-algorithm/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

## Format: `[ID] [P] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

## Phase 1: Setup

**Purpose**: Verify environment is ready

- [x] T001 Ensure Docker is up and existing tests pass: `docker compose exec web uv run pytest tests/test_reservations.py::TestAutoDate -v`

---

## Phase 2: User Story 1 - Next-Week Auto-Date (Priority: P1) 🎯 MVP

**Goal**: Change the auto-date algorithm so selecting a class slot always sets the date to the same day-of-week in the following week (never the current week).

**Independent Test**: Create a reservation on any day, select a class slot with a future day-of-week later this week, verify the date is set to the following week (not this week).

### TDD: Write test FIRST, confirm RED, then implement

- [x] T002 [US1] Update `test_future_day_this_week` in `backend/tests/test_reservations.py` to expect the future-day date to be in the following week (current diff + 7). Run test — confirm it FAILS (RED) because implementation still uses old algorithm.
- [x] T003 [US1] Change JS algorithm in `backend/apps/reservations/static/reservations/js/auto-date.js` — update `autoDate()` so future-day case adds 7 to `daysAhead` (always next week).
- [x] T004 [US1] Change Python algorithm in `backend/apps/reservations/views.py` — update `auto_date_for_slot()` to match new JS logic for future-day case.
- [x] T005 [US1] Run full `TestAutoDate` test suite — confirm all tests PASS (GREEN).

**Checkpoint**: Auto-date algorithm now always sets date to following week.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and session recording

- [x] T006 Run quickstart.md validation — confirm JS + Python algorithm changes produce correct dates per spec acceptance scenarios
- [x] T007 [P] Save AI session file to `ai/sessions/`
- [x] T008 [P] Move feature todo file if applicable (N/A — no todo file)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — verify environment
- **User Story 1 (Phase 2)**: Depends on Phase 1
- **Polish (Phase 3)**: Depends on Phase 2

### Within User Story 1

- T002 (update test) MUST be done before T003/T004 (change implementation)
- T003 and T004 (JS + Python) can run in parallel
- T005 (verify GREEN) MUST be done after implementation

### Parallel Opportunities

- T003 and T004 can run in parallel (different files, no dependencies)
- T007 and T008 can run in parallel

## Implementation Strategy

### MVP Scope: User Story 1 only

1. Complete Phase 1: Setup
2. Complete Phase 2: User Story 1
3. Complete Phase 3: Polish

## Environment Reference

- **Run tests**: `docker compose exec web uv run pytest`
- **Specific test class**: `docker compose exec web uv run pytest tests/test_reservations.py::TestAutoDate -v`
