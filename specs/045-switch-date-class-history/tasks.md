# Tasks: Switch date and class block columns in history

**Input**: Design documents from `/specs/045-switch-date-class-history/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

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

## Phase 3: User Story 1 - Reorder reservation history columns on client detail (Priority: P1) 🎯 MVP

**Goal**: Reorder the "Historial de Reservas" table columns on `clients/{id}/` to Clase, Fecha, Equipo

**Independent Test**: Navigate to any client detail page and verify columns appear as Clase, Fecha, Equipo in the `<thead>` of the reservation history table

### Tests for User Story 1 (TDD — write FIRST, ensure they FAIL before implementation)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T001 [P] [US1] Write test for column order on client detail page in `backend/tests/test_client_detail.py` — verify `<thead>` contains Clase, Fecha, Equipo in order
- [ ] T002 [P] [US1] Write test for empty reservations state in `backend/tests/test_client_detail.py` — verify empty state message renders when client has no reservations

### Implementation for User Story 1

- [ ] T003 [US1] Reorder `<th>` and `<td>` elements in `backend/apps/clients/templates/clients/client_detail.html` — move Class before Date, resulting order: Class, Date, Equipment

**Checkpoint**: User Story 1 should be fully functional and testable independently. Run `docker compose exec web uv run pytest backend/tests/test_client_detail.py -v` to verify.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T004 Update the feature todo file: move `ai/features/todos/18_switch_date_and_class_block_in_history.md` to `ai/features/done/`
- [ ] T005 [P] Save AI session file to `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — N/A
- **Foundational (Phase 2)**: No dependencies — N/A
- **User Story 1 (Phase 3)**: No dependencies — can proceed immediately
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories

### Within User Story

- Tests (T001, T002) MUST be written and FAIL before implementation (T003)
- Commit after each task or logical group

### Parallel Opportunities

- T001 and T002 can run in parallel (different test methods in same file, but typically written sequentially)
- T004 and T005 can run in parallel (different files, no dependencies)

---

## Parallel Example: User Story 1

```bash
# Write both tests together:
Task: "Write column order test in backend/tests/test_client_detail.py"
Task: "Write empty state test in backend/tests/test_client_detail.py"

# After tests fail, implement:
Task: "Reorder columns in backend/apps/clients/templates/clients/client_detail.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write tests T001, T002 — verify they fail
2. Implement T003 — verify tests pass
3. Run full test suite
4. Stop and validate

### Incremental Delivery

1. Write + implement all at once (single story, small scope)

### Environment Reference

- **Run tests**: `docker compose exec web uv run pytest backend/tests/test_client_detail.py -v`
- **Full suite**: `docker compose exec web uv run pytest`
- **No migrations or package changes required**

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
