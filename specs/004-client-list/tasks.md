---

description: "Task list for adding client list with pagination, edit functionality, and counter to clients/search/"

---

# Tasks: Client List in Client Search

**Input**: Design documents from `specs/004-client-list/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are included per the constitution's TDD requirement (Testing Standards — NON-NEGOTIABLE).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/`, `backend/tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No setup needed — project and apps already exist.

All infrastructure is already in place: Django project, Client model, views, URLs, templates, and test runner. This phase is empty.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites — the `clients/search/` endpoint, Client model, and template all exist.

---

## Phase 3: User Story 1 - View paginated client list (Priority: P1) 🎯 MVP

**Goal**: Operator sees a paginated list of all clients with all attributes when visiting `clients/search/`.

**Independent Test**: Navigate to `clients/search/` — verify the list shows all Client attributes. Create 21 clients, reload — verify pagination shows 10 on page 1, 10 on page 2, 1 on page 3.

### Tests for User Story 1 ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T001 [P] [US1] Test that clients/search/ renders all clients when no search query is given in `backend/tests/test_client_list.py`
- [X] T002 [P] [US1] Test that client list shows all Client model attributes in `backend/tests/test_client_list.py`
- [X] T003 [P] [US1] Test pagination: 21 clients split into 3 pages (10, 10, 1) in `backend/tests/test_client_list.py`
- [X] T004 [P] [US1] Test pagination controls appear only when >10 clients in `backend/tests/test_client_list.py`
- [X] T005 [P] [US1] Test empty state message displays when 0 clients in `backend/tests/test_client_list.py`
- [X] T006 [P] [US1] Test search still works alongside full list in `backend/tests/test_client_list.py`

### Implementation for User Story 1

- [X] T007 [US1] Update `client_search` view to show all clients with Django `Paginator` in `backend/apps/clients/views.py`
- [X] T008 [US1] Add all Client attributes (name, email, mobile, is_active, dates) to the list table in `backend/apps/clients/templates/clients/search.html`
- [X] T009 [US1] Add Bootstrap pagination navigation (Next/Previous, page numbers) below the table in `backend/apps/clients/templates/clients/search.html`
- [X] T010 [US1] Add empty state message when no clients exist in `backend/apps/clients/templates/clients/search.html`

**Checkpoint**: At this point, the paginated client list should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Edit a client from the list (Priority: P1)

**Goal**: Operator clicks an Edit button on any client row to modify that client's details.

**Independent Test**: On `clients/search/`, click the Edit button on any row — verify it navigates to the Django admin change form for that client.

### Tests for User Story 2 ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T011 [P] [US2] Test each client row has an Edit link/button in `backend/tests/test_client_list.py`
- [X] T012 [P] [US2] Test Edit link navigates to admin change form for correct client in `backend/tests/test_client_list.py`

### Implementation for User Story 2

- [X] T013 [US2] Add Edit button to each client row linking to admin change view in `backend/apps/clients/templates/clients/search.html`

**Checkpoint**: Operators can now navigate from any client row to the edit form.

---

## Phase 5: User Story 3 - View client counter widget (Priority: P2)

**Goal**: Operator sees a counter widget on `clients/search/` showing total number of clients.

**Independent Test**: On `clients/search/`, verify the counter value matches the actual client count in the database.

### Tests for User Story 3 ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T014 [P] [US3] Test counter widget displays total client count in `backend/tests/test_client_list.py`
- [X] T015 [P] [US3] Test counter updates when clients are added/deleted in `backend/tests/test_client_list.py`

### Implementation for User Story 3

- [X] T016 [US3] Pass `client_count` to template context in `backend/apps/clients/views.py`
- [X] T017 [US3] Add counter widget (e.g., "Total clients: 42") above the client list in `backend/apps/clients/templates/clients/search.html`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify everything works together.

- [X] T018 [P] Verify existing search-by-email/mobile still works (regression check)
- [X] T019 Update `specs/004-client-list/quickstart.md` with any new verification steps
- [X] T020 Run full test suite to confirm no regressions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Empty — no work needed
- **Foundational (Phase 2)**: Empty — no work needed
- **User Story 1 (Phase 3)**: Can start immediately — modifies `views.py` and `search.html`
- **User Story 2 (Phase 4)**: Depends on US1 (same template file)
- **User Story 3 (Phase 5)**: Depends on US1 (same view and template)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — can start immediately
- **User Story 2 (P1)**: Depends on US1 — modifies the same table rows in the template
- **User Story 3 (P2)**: Depends on US1 — adds counter to same template/view

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- View logic before template changes

### Parallel Opportunities

- Tests within each story marked [P] can run in parallel (different test cases in same file)
- No cross-story parallelism — all stories touch the same 2 files (`views.py`, `search.html`)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test that clients/search/ renders all clients when no search query is given"
Task: "Test that client list shows all Client model attributes"
Task: "Test pagination: 21 clients split into 3 pages (10, 10, 1)"
Task: "Test pagination controls appear only when >10 clients"
Task: "Test empty state message displays when 0 clients"
Task: "Test search still works alongside full list"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 (paginated client list)
2. **STOP and VALIDATE**: Test the paginated list independently
3. Deploy/demo if ready — this is the MVP

### Incremental Delivery

1. Add paginated client list (US1) → Test → Deploy/Demo (MVP!)
2. Add Edit button per row (US2) → Test → Deploy/Demo
3. Add counter widget (US3) → Test → Deploy/Demo
4. Each story adds value without breaking previous stories

### Note on TDD

Per the constitution (Testing Standards — NON-NEGOTIABLE), tests MUST be written and reviewed by the user FIRST, and MUST fail before implementation begins.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
