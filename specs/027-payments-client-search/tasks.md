---

description: "Task list for payments client search feature"

---

# Tasks: Payments Client Search

**Input**: Design documents from `specs/027-payments-client-search/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD is mandatory per project constitution. Tests must be written and reviewed by the user FIRST, and must fail before implementation begins.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Create directory structure for new files

- [X] T001 Create `partials/` directory under `backend/apps/payments/templates/payments/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Form definition and test infrastructure that blocks all user stories

- [X] T002 [P] Create `PaymentSearchForm` with a single `q` CharField in `backend/apps/payments/forms.py`
- [X] T003 [P] Write failing tests for search functionality in `backend/tests/test_payments_search.py`

**Checkpoint**: Form and test file ready — user story implementation can begin

---

## Phase 3: User Story 1 - Search payments by client (Priority: P1) 🎯 MVP

**Goal**: Operator types client name, email, or mobile into a search field on the payments page and sees matching payments in the grid. Search is case-insensitive, requires 3+ characters, uses HTMX 300ms debounce, and has an explicit submit button.

**Independent Test**: Enter 3+ characters of a client's name in the search field and verify payments for matching clients appear in the grid without a full page reload.

### Tests for User Story 1 (TDD — write first, ensure FAIL, then implement) ⚠️

- [X] T004 [P] [US1] Write failing integration test for search by client name in `backend/tests/test_payments_search.py`
- [X] T005 [P] [US1] Write failing integration test for search by client email in `backend/tests/test_payments_search.py`
- [X] T006 [P] [US1] Write failing integration test for search by client mobile in `backend/tests/test_payments_search.py`
- [X] T007 [P] [US1] Write failing integration test for 3-character minimum in `backend/tests/test_payments_search.py`
- [X] T008 [P] [US1] Write failing integration test for case-insensitive matching in `backend/tests/test_payments_search.py`
- [X] T009 [P] [US1] Write failing integration test excluding inactive clients in `backend/tests/test_payments_search.py`

### Implementation for User Story 1

- [X] T010 [US1] Modify `PaymentListView.get_queryset()` in `backend/apps/payments/views.py` to filter by `q` param using client name/email/mobile icontains, requiring 3+ characters, excluding inactive clients
- [X] T011 [US1] Modify `PaymentListView.get_context_data()` in `backend/apps/payments/views.py` to pass `q` and `not_found` to template context
- [X] T012 [P] [US1] Modify `backend/apps/payments/templates/payments/payment_list.html` to replace client ID input with HTMX search form (hx-get, hx-trigger="keyup changed delay:300ms", submit button, clear button)
- [X] T013 [US1] Create `_payment_search_results.html` partial template in `backend/apps/payments/templates/payments/partials/_payment_search_results.html` for HTMX results swap
- [X] T014 [US1] Add i18n strings for search placeholder, labels, and messages in `backend/locale/es/LC_MESSAGES/django.po`
- [X] T015 [US1] Compile translations by running `django-admin compilemessages` in the backend directory
- [X] T016 [US1] Make failing tests pass by implementing the search query logic

**Checkpoint**: Search by client name, email, or mobile works on the payments page. Grid format and pagination are preserved.

---

## Phase 4: User Story 2 - No results handling (Priority: P2)

**Goal**: When no payments match the search criteria, the operator sees a clear "NOT FOUND" message in the grid area. When the search field is cleared, the grid returns to showing all payments.

**Independent Test**: Enter a search term that matches no client and verify a "NOT FOUND" message is displayed in the grid area. Then clear the field and verify all payments reappear.

### Tests for User Story 2 (TDD — write first, ensure FAIL, then implement) ⚠️

- [X] T017 [P] [US2] Write failing integration test for NOT FOUND message in `backend/tests/test_payments_search.py`
- [X] T018 [P] [US2] Write failing integration test for grid returning to all payments when search is cleared in `backend/tests/test_payments_search.py`

### Implementation for User Story 2

- [X] T019 [US2] Add NOT FOUND alert-warning block to `_payment_search_results.html` partial in `backend/apps/payments/templates/payments/partials/_payment_search_results.html`
- [X] T020 [US2] Ensure clear button resets `q` param and shows all payments (the Clear link already exists in `payment_list.html`)
- [X] T021 [US2] Make failing tests pass

**Checkpoint**: No-results empty state shows clear feedback. Search clearance restores full grid.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final touches that span multiple user stories

- [X] T022 [P] Verify pagination links preserve `?q=` parameter in both full-page and HTMX responses
- [X] T023 [P] Add `aria-live="polite"` and `aria-atomic="true"` to search results container for accessibility
- [X] T024 Run linting (`ruff check`) on all modified files in `backend/`
- [X] T025 Run full test suite and verify all tests pass
- [X] T026 Move `ai/features/todos/11_Payments_client_search.md` to `ai/features/done/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Story 1 (Phase 3)**: Depends on Phase 2 — core search functionality
- **User Story 2 (Phase 4)**: Depends on Phase 3 — no-results state builds on search
- **Polish (Phase 5)**: Depends on both Phase 3 and Phase 4

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — core search feature, no dependencies on other stories
- **User Story 2 (P2)**: Can start after US1 — builds on the search infrastructure

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Form → View logic → Template → Partial → i18n
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T002 and T003 can run in parallel (form + tests are independent files)
- T004 through T009 (tests) can all run in parallel
- T012 (template) can run in parallel with T010/T011 (view logic)
- T017 and T018 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write failing test for search by name"
Task: "Write failing test for search by email"
Task: "Write failing test for search by mobile"
Task: "Write failing test for 3-char minimum"
Task: "Write failing test for case-insensitive"
Task: "Write failing test for inactive exclusion"

# Launch view + template tasks in parallel:
Task: "Modify PaymentListView.get_queryset() in views.py"
Task: "Modify payment_list.html with HTMX search form"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (trivial)
2. Complete Phase 2: Foundational (form + tests)
3. Complete Phase 3: User Story 1 (search by name, email, mobile)
4. **STOP and VALIDATE**: Test search independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (search) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (no results) → Test independently → Deploy/Demo

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Spanish is the only configured locale — all i18n goes to `backend/locale/es/LC_MESSAGES/django.po`
