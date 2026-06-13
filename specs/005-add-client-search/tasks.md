---

description: "Task list for adding client search by name"
---

# Tasks: Add Client Search by Name

**Input**: Design documents from `specs/005-add-client-search/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: All tasks include test tasks per Constitution II (TDD mandatory).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow the plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Add HTMX script tag to `backend/templates/base.html` (CDN script before `</head>`)
- [x] T002 [P] Update `ClientSearchForm` label from "Email or mobile number..." to "Search clients..." in `backend/apps/clients/forms.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create HTMX partial template `backend/apps/clients/templates/clients/_search_results.html` containing the results table, pagination, and counter from `search.html`
- [x] T004 [P] Update `backend/apps/clients/templates/clients/search.html` to include the partial and add HTMX attributes (`hx-get`, `hx-trigger`, `hx-target`, `hx-select`) to the search form

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Search client by name (Priority: P1) 🎯 MVP

**Goal**: Operator types 3+ characters and matching clients appear in results. Search is case-insensitive and searches first_name and last_name.

**Independent Test**: Enter a partial client name (3+ chars) → verify matching clients appear in results.

### Tests for User Story 1 (TDD — write first, ensure fail before implementation) ⚠️

- [x] T005 [P] [US1] Test that searching by first name partial match returns matching client in `backend/tests/test_client_search_name.py`
- [x] T006 [P] [US1] Test that searching by last name partial match returns matching client in `backend/tests/test_client_search_name.py`
- [x] T007 [P] [US1] Test that search is case-insensitive (e.g., "MAR" matches "mark") in `backend/tests/test_client_search_name.py`
- [x] T008 [P] [US1] Test that fewer than 3 characters does NOT trigger name search in `backend/tests/test_client_search_name.py`
- [x] T009 [P] [US1] Test that search across both first_name and last_name works in `backend/tests/test_client_search_name.py`

### Implementation for User Story 1

- [x] T010 [US1] Extend `client_search` view filter in `backend/apps/clients/views.py` to include `Q(first_name__icontains=q) | Q(last_name__icontains=q)` when `len(q) >= 3`
- [x] T011 [US1] Add HTMX-aware response in `backend/apps/clients/views.py`: return partial template when `request.headers.get("HX-Request")` is present

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — See search term highlighted in results (Priority: P1)

**Goal**: Matched text in client names is visually highlighted with bold + background color.

**Independent Test**: Search for a name fragment and verify the fragment is wrapped in `<mark>` tags in the response HTML.

### Tests for User Story 2 (TDD — write first, ensure fail before implementation) ⚠️

- [x] T012 [P] [US2] Test that matched search term is wrapped in `<mark>` tags in `backend/tests/test_client_search_name.py`
- [x] T013 [P] [US2] Test that highlighting is case-insensitive in `backend/tests/test_client_search_name.py`
- [x] T014 [P] [US2] Test that multiple occurrences in same name are highlighted in `backend/tests/test_client_search_name.py`

### Implementation for User Story 2

- [x] T015 [US2] Create Django template filter or helper function to wrap matched text in `<mark>` tags (bold + background) and apply it to name fields in `backend/apps/clients/templates/clients/_search_results.html`

**Checkpoint**: At this point, User Story 2 should be independently testable

---

## Phase 5: User Story 3 — No results handling (Priority: P1)

**Goal**: "Client NOT FOUND" message displays when no client matches.

**Independent Test**: Enter a name that matches no client → verify "Client NOT FOUND" appears.

### Tests for User Story 3 (TDD — write first, ensure fail before implementation) ⚠️

- [x] T016 [P] [US3] Test that "Client NOT FOUND" message appears when no results match in `backend/tests/test_client_search_name.py`
- [x] T017 [P] [US3] Test that "Client NOT FOUND" disappears when search is modified to match a client in `backend/tests/test_client_search_name.py`

### Implementation for User Story 3

- [x] T018 [US3] Add alert for "Client NOT FOUND" in `backend/apps/clients/templates/clients/_search_results.html` when results are empty and a search query exists

**Checkpoint**: All P1 user stories should now be independently functional

---

## Phase 6: User Story 4 — Search by email or mobile still works (Priority: P2)

**Goal**: Existing email and mobile search continues to work unchanged alongside name search.

**Independent Test**: Search by email or mobile that exists → verify matching client appears.

### Tests for User Story 4 (TDD — write first, ensure fail before implementation) ⚠️

- [x] T019 [P] [US4] Test that searching by existing email returns matching client in `backend/tests/test_client_search_name.py`
- [x] T020 [P] [US4] Test that searching by existing mobile number returns matching client in `backend/tests/test_client_search_name.py`
- [x] T021 [P] [US4] Test that combined name+email search works in `backend/tests/test_client_search_name.py`

### Implementation for User Story 4

- [x] T022 [US4] Verify existing email and mobile filter logic remains intact in `backend/apps/clients/views.py` (regression guard — no code change needed if filter is correctly extended)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T023 Add `aria-live="polite"` region to search results container for WCAG 2.1 AA screen reader announcements in `backend/apps/clients/templates/clients/_search_results.html`
- [x] T024 [P] Ensure all new strings use Django i18n (`{% translate %}` / `_()`) in templates and views
- [x] T025 Run `pytest tests/test_client_search_name.py -v` and fix any failures
- [x] T026 Run `ruff check backend/` and fix any linting issues
- [x] T027 Move the feature todo file from `ai/features/todos/` to `ai/features/done/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 can be done first (core search)
  - US2 (highlighting) depends on US1 view changes
  - US3 (NOT FOUND) depends on US1 view changes
  - US4 (regression tests) can proceed alongside or after US1
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No external dependencies
- **User Story 2 (P1)**: Depends on US1 view changes (needs the updated view filter)
- **User Story 3 (P1)**: Depends on US1 view changes (needs the query + partial template)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) — tests only, no code changes

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Implementation follows: model queries → template logic → endpoint integration
- Story complete before moving to next priority

### Parallel Opportunities

- T001 (HTMX script) and T002 (form label) can run in parallel
- T003 (partial template) and T004 (HTMX form attrs) can run in parallel
- All tests within a user story marked [P] can run in parallel
- US4 regression tests can be written in parallel with US1 implementation

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test first name search in backend/tests/test_client_search_name.py"
Task: "Test last name search in backend/tests/test_client_search_name.py"
Task: "Test case-insensitive search in backend/tests/test_client_search_name.py"
Task: "Test 3-char minimum in backend/tests/test_client_search_name.py"
Task: "Test cross-field search in backend/tests/test_client_search_name.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (HTMX + form label)
2. Complete Phase 2: Foundational (partial template + HTMX attrs)
3. Complete Phase 3: User Story 1 (name search + HTMX response)
4. **STOP and VALIDATE**: Test US1 independently
5. Deploy/demo if ready — basic name search works with real-time results

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 (name search) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (highlighting) → Test independently → Deploy/Demo
4. Add User Story 3 (NOT FOUND) → Test independently → Deploy/Demo
5. Add User Story 4 (regression tests) → Test independently → Deploy/Demo

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (view + HTMX)
   - Developer B: User Story 2 (highlighting filter) — starts after US1 view is stable
   - Developer C: User Story 4 (regression tests) — can write tests immediately
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD per Constitution II)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- HTMX script loaded from CDN — no pip install needed
- All existing search tests in `test_client_list.py` must continue to pass
