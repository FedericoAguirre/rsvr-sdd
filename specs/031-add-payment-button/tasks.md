# Tasks: Add Payment Button to Client Page

**Input**: Design documents from `/specs/031-add-payment-button/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per Constitution §II (TDD is mandatory). Tests MUST be written and fail BEFORE implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Path Conventions

- **Django web app**: `backend/apps/` for app code, `backend/tests/` for tests
- All paths below follow the project structure from plan.md

---

**⚠️ NOTE**: This feature has no Setup or Foundational phases — it is an incremental change to an existing Django project. All code changes are limited to two files (one template, one view) and one new test file.

---

## Phase 1: User Story 1 - Create Payment from Client Detail Page (Priority: P1) 🎯 MVP

**Goal**: Add a **New Payment** button to the client detail page that navigates to `payments/create/` with the current client preselected in the combo box.

**Independent Test**: Navigate to any `clients/{pk}/` page — confirm a **New Payment** button appears to the right of **Nueva Reserva**; click it and verify the `payments/create/` page loads with the client combo box pre-filled with that client.

### Tests for User Story 1 ⚠️

> **IMPORTANT**: Write these tests FIRST, ensure they FAIL before any implementation

- [X] T001 [P] [US1] Write test for New Payment button presence and position on client detail page in `backend/tests/test_payments_create_button.py`
- [X] T002 [P] [US1] Write test for New Payment button href containing `?client=<pk>` in `backend/tests/test_payments_create_button.py`
- [X] T003 [P] [US1] Write test for client preselection on PaymentCreateView via `?client=` query param in `backend/tests/test_payments_create_button.py`

### Implementation for User Story 1

- [X] T004 [US1] Add `get_initial()` override to `PaymentCreateView` in `backend/apps/payments/views.py` to pre-populate `client` field from `?client=` query parameter
- [X] T005 [P] [US1] Add **New Payment** button `<a>` after **Nueva Reserva** in `backend/apps/clients/templates/clients/client_detail.html` with `href="{% url 'payments:create' %}?client={{ client.pk }}"` and `btn btn-success mb-3` classes
- [X] T006 [US1] Run tests to confirm T001-T003 pass (Red-Green-Refactor cycle complete)

**Checkpoint**: Client detail page has a **New Payment** button. Clicking it navigates to `payments/create/` with the correct client preselected. All tests pass.

---

## Phase 2: User Story 2 - Create Payment with No Client (Direct Access - Priority: P2)

**Goal**: Verify that direct access to `payments/create/` (without `?client=` parameter) still works with an empty client field.

**Independent Test**: Navigate directly to `/payments/create/` — confirm the client combo box is empty and a payment can be created without any client preselected.

### Tests for User Story 2 ⚠️

- [X] T007 [P] [US2] Write regression test for direct access to `payments/create/` with empty client field in `backend/tests/test_payments_create_button.py`

### Implementation for User Story 2

- [X] T008 [US2] Run regression test to confirm direct access behavior is preserved (T007 passes)

**Checkpoint**: Direct access to `payments/create/` continues to work with no client preselected. Regression test passes.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and consistency checks

- [X] T009 [P] Verify i18n — confirm `{% translate "New Payment" %}` renders as "Nuevo pago" in the template (key already exists in `backend/locale/es/LC_MESSAGES/django.po`)
- [X] T010 Run `ruff check backend/` and fix any linting issues
- [X] T011 Run full test suite to confirm no regressions

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 1)**: Can start immediately — no setup or foundational dependencies
- **User Story 2 (Phase 2)**: Depends on US1 completion (same view modified)
- **Polish (Phase 3)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories — fully independent MVP
- **User Story 2 (P2)**: Requires US1 view modifications to be in place (same `PaymentCreateView`)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Implementation follows the research.md decisions

### Parallel Opportunities

- T001, T002, T003 can run in parallel (test writing)
- T005 is independent of T004 (different files) — marked [P]
- T009 is independent of T010, T011 (different concerns) — marked [P]

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 in parallel:
Task: "Write test for button presence and position in backend/tests/test_payments_create_button.py"
Task: "Write test for button href in backend/tests/test_payments_create_button.py"
Task: "Write test for client preselection in backend/tests/test_payments_create_button.py"

# Launch view and template changes in parallel:
Task: "Add get_initial() to PaymentCreateView in backend/apps/payments/views.py"
Task: "Add New Payment button to client_detail.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: User Story 1
2. **STOP and VALIDATE**: Test button presence, navigation, and client preselection
3. Deploy/demo if ready

### Incremental Delivery

1. User Story 1 (button + preselection) → Test independently → Deploy/Demo (MVP!)
2. User Story 2 (regression verification) → Test independently → Deploy

---

## Notes

- No new models, migrations, URL patterns, or translation keys needed
- The `"New Payment"` / `"Nuevo pago"` key already exists in `django.po` — no i18n registration needed
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD per Constitution §II)
