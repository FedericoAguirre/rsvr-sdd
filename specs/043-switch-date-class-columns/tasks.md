# Tasks: Switch Date and Class Block Columns in Payments History

**Input**: Design documents from `/specs/043-switch-date-class-columns/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are included per constitution requirement (TDD is mandatory).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/`, `backend/tests/`
- Single template file change in `backend/apps/clients/templates/clients/client_detail.html`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — N/A for this feature, project is already set up

*No setup tasks required.*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure — N/A, no new models, migrations, or services needed

*No foundational tasks required.*

---

## Phase 3: User Story 1 - Reorder Reservation History Columns (Priority: P1) 🎯 MVP

**Goal**: Reorder the reservation history table columns on the client detail page from current order (Date, Class, Equipment) to desired order (Class, Date, Equipment).

**Independent Test**: Load any client detail page with reservations and verify the column headers appear in the order: Clase, Fecha, Equipo.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [P] [US1] Write test for column order on client detail page in `backend/tests/test_client_detail.py`
- [x] T002 [P] [US1] Write test for column order with empty reservation list in `backend/tests/test_client_detail.py`

### Implementation for User Story 1

- [x] T003 [US1] Reorder `<th>` and `<td>` elements in `backend/apps/clients/templates/clients/client_detail.html` from `Date/Class/Equipment` to `Class/Date/Equipment`

**Checkpoint**: User Story 1 should be fully functional and testable independently. Run `docker compose exec web uv run pytest backend/tests/test_client_detail.py -v` to verify.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T004 Update the feature todo file: move `ai/features/todos/18_switch_date_and_class_block_in_history.md` to `ai/features/done/`
- [x] T005 [P] Save AI session file to `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 3)**: No dependencies — can start immediately
- **Polish (Phase 4)**: Depends on User Story 1 being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — standalone, single-file change

### Within User Story 1

- Tests MUST be written and FAIL before implementation
- Implementation after tests

### Parallel Opportunities

- T001 and T002 can run in parallel (same file, different test functions)
- T004 and T005 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test for column order on client detail page in backend/tests/test_client_detail.py"
Task: "Write test for column order with empty reservation list in backend/tests/test_client_detail.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 — Write tests (fail) → Implement → Verify (pass)
2. Complete Phase 4: Polish

### Incremental Delivery

1. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
2. Each story adds value without breaking previous stories

### Environment Reference

When writing script fragments, task execution steps, or running the code, always use these exact commands:
- **Run tests**: `docker compose exec web uv run pytest backend/tests/test_client_detail.py -v`
- **Run all tests**: `docker compose exec web uv run pytest`
- **Check migrations**: `docker compose exec web uv run manage.py showmigrations`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
