---

description: "Task list for extending filter highlighting to email and mobile"
---

# Tasks: Extend Filter Highlighting to Email and Mobile

**Input**: Design documents from `/specs/015-filter-highlighting-extend/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Included per constitution requirement (TDD mandatory).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Django project root at `backend/`
- Client app: `backend/apps/clients/`
- Tests: `backend/tests/`
- Template filters: `backend/apps/clients/templatetags/`
- Templates: `backend/apps/clients/templates/clients/`

## Phase 1: Setup

**Purpose**: Verify environment ready for implementation

- [x] T001 Verify branch `017-filter-highlighting-extend` checked out and project builds with `make build` and `make up`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Template filter enhancement needed before mobile highlighting can work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Enhance `highlight` filter in `backend/apps/clients/templatetags/client_extras.py` to support mobile number normalization: strip all non-numeric characters from both the query and the stored value before matching, then apply `<mark>` tags around matched digits in the original formatted string

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 - Email search shows highlighted results (Priority: P1) 🎯 MVP

**Goal**: When Operator searches by email, matched portions are highlighted in the email column.

**Independent Test**: Search for a partial email address (e.g., "john") and verify the `<mark>` tag wraps the matched fragment in the email column of every result.

### Tests for User Story 1

> **Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Write test for email partial match highlighting: verify `|highlight:q` wraps matched substring in `<mark>` tags in `backend/tests/test_client_search_highlighting.py`
- [x] T004 [P] [US1] Write test for email case-insensitive highlighting: verify uppercase search matches lowercase emails in `backend/tests/test_client_search_highlighting.py`
- [x] T005 [P] [US1] Write test for email with <3 chars: verify no highlighting applied for short queries in `backend/tests/test_client_search_highlighting.py`

### Implementation for User Story 1

- [x] T006 [US1] Apply `|highlight:q` to `c.email` cell in `backend/apps/clients/templates/clients/_search_results.html`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mobile number search shows highlighted results (Priority: P1) 🎯 MVP

**Goal**: When Operator searches by mobile number, matched digits are highlighted in the mobile column.

**Independent Test**: Search for a partial mobile number (e.g., "555") and verify the matching digits are highlighted in the formatted display value (e.g., "+1 (555) 123-4567" shows `<mark>555</mark>`).

### Tests for User Story 2

> **Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [P] [US2] Write test for mobile partial digit match: verify non-numeric characters stripped before matching in `backend/tests/test_client_search_highlighting.py`
- [x] T008 [P] [US2] Write test for mobile with formatting characters: verify "555" matches "+1 (555) 123-4567" and highlights digits in `backend/tests/test_client_search_highlighting.py`
- [x] T009 [P] [US2] Write test for mobile with <3 chars: verify no highlighting applied for short queries in `backend/tests/test_client_search_highlighting.py`

### Implementation for User Story 2

- [x] T010 [US2] Apply `|highlight:q` to `c.mobile` cell in `backend/apps/clients/templates/clients/_search_results.html`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Consistency with existing name search highlighting (Priority: P2)

**Goal**: Email and mobile highlighting visually matches the existing name search highlighting.

**Independent Test**: Compare rendered HTML of name, email, and mobile cells — all should use the same `<mark>` tag styling.

### Tests for User Story 3

> **Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US3] Write test verifying same `<mark>` tag style is used across name, email, and mobile fields in `backend/tests/test_client_search_highlighting.py`
- [x] T012 [P] [US3] Write test verifying name search highlighting still renders `<mark>` tags identically to before in `backend/tests/test_client_search_highlighting.py`

### Implementation for User Story 3

- [x] T013 [US3] Verify and fix any visual inconsistencies (same filter function, no per-field differences)

**Checkpoint**: User Stories 1, 2, AND 3 should work independently

---

## Phase 6: User Story 4 - All search fields remain functional (Priority: P2)

**Goal**: Existing name search highlighting and full search workflow unchanged.

**Independent Test**: Perform a name search and verify highlighting works identically before and after changes.

### Tests for User Story 4

> **Write these tests FIRST, ensure they FAIL before implementation**

- [x] T014 [P] [US4] Write integration test: full search flow by name returns highlighted name + email + mobile results in `backend/tests/test_client_search_highlighting.py`
- [x] T015 [P] [US4] Write integration test: search by each field type independently still returns correct results in `backend/tests/test_client_search_highlighting.py`
- [x] T016 [P] [US4] Write test: clearing search removes all highlighting in `backend/tests/test_client_search_highlighting.py`

### Implementation for User Story 4

- [x] T017 [US4] Run existing `test_client_search_name.py` and verify all tests still pass

**Checkpoint**: All user stories functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, documentation, and quality checks

- [x] T018 [P] Create compressed AI session file in `ai/sessions/` per constitution requirements
- [x] T019 Move `ai/features/todos/05_Filter_highlighting.md` to `ai/features/done/`
- [x] T020 Run Ruff linting on `backend/` and fix any issues
- [x] T021 Run full test suite: `cd backend && python -m pytest tests/ -v`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (P1) and US2 (P1) can proceed in parallel
  - US3 (P2) and US4 (P2) can be validated after US1/US2
- **Polish (Final)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational — independent of US1 (different template cells)
- **User Story 3 (P2)**: Depends on US1 and US2 (verifies consistency across all three fields)
- **User Story 4 (P2)**: Depends on US1 and US2 (regression verification)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Template changes before verification

### Parallel Opportunities

- Test tasks within a story marked [P] can run in parallel
- US1 and US2 can run in parallel since they modify different template cells and test file additions are append-only
- US3 and US4 share a test file with US1/US2 — serialize or merge test additions

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test for email partial match highlighting in backend/tests/test_client_search_highlighting.py"
Task: "Write test for email case-insensitive highlighting in backend/tests/test_client_search_highlighting.py"
Task: "Write test for email with <3 chars in backend/tests/test_client_search_highlighting.py"

# Then implement:
Task: "Apply |highlight:q to c.email cell in backend/apps/clients/templates/clients/_search_results.html"
```

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Write test for mobile partial digit match in backend/tests/test_client_search_highlighting.py"
Task: "Write test for mobile with formatting characters in backend/tests/test_client_search_highlighting.py"
Task: "Write test for mobile with <3 chars in backend/tests/test_client_search_highlighting.py"

# Then implement:
Task: "Apply |highlight:q to c.mobile cell in backend/apps/clients/templates/clients/_search_results.html"
```

---

## Implementation Strategy

### MVP First (User Stories 1 and 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — T002 blocks everything)
3. Complete Phase 3: User Story 1 (email highlighting)
4. Complete Phase 4: User Story 2 (mobile highlighting)
5. **STOP and VALIDATE**: Test both US1 and US2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (email highlighting) → Test independently → Deploy/Demo (MVP!)
3. Add US2 (mobile highlighting) → Test independently → Deploy/Demo
4. Add US3 (consistency) → Verify → Deploy
5. Add US4 (regression) → Verify → Deploy
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. One developer: Phase 2 (Foundational — template tag enhancement)
2. Once Foundational is done:
   - Developer A: User Story 1 (email)
   - Developer B: User Story 2 (mobile)
3. Either developer: User Stories 3 and 4 (consistency check)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
