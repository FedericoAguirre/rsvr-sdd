# Tasks: Payments Associate Button

**Input**: Design documents from `specs/029-payments-associate-button/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/README.md, quickstart.md

**Tests**: Included per constitution TDD requirement: tests MUST be written and reviewed before implementation.

**Organization**: Single user story — one phase.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root
- `backend/apps/payments/`, `backend/tests/`, `locale/`

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [X] T001 Verify current branch is `029-payments-associate-button` and working tree is clean

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Prerequisites for the user story

- [X] T002 [P] Add `Associate` → `Asociar` i18n key in `locale/es/LC_MESSAGES/django.po`

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 - Associate Payment via Button (Priority: P1) 🎯 MVP

**Goal**: Operators see an Associate button on the payment detail page (left of Edit) and can navigate to the associate page to link reservations to the payment.

**Independent Test**: Navigate to any payment detail page, confirm Associate button appears left of Edit, click it to verify navigation to the associate page with 200 status.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T003 [P] [US1] Test Associate button presence and position relative to Edit in `backend/tests/test_payments_associate_button.py`
- [X] T004 [P] [US1] Test Associate button href points to `payments:associate` URL in `backend/tests/test_payments_associate_button.py`
- [X] T005 [P] [US1] Test GET `/payments/<pk>/associate/` returns 200 in `backend/tests/test_payments_associate_button.py`
- [X] T006 [P] [US1] Test GET `/payments/<pk>/associate/` includes available reservations context in `backend/tests/test_payments_associate_button.py`
- [X] T007 [P] [US1] Test tab order (Associate before Edit) in `backend/tests/test_payments_associate_button.py`

### Implementation for User Story 1

- [X] T008 [US1] Add `get()` method to `PaymentAssociateView` in `backend/apps/payments/views.py` that renders available reservations
- [X] T009 [US1] Create `payment_associate.html` template in `backend/apps/payments/templates/payments/payment_associate.html`
- [X] T010 [US1] Insert Associate button `<a>` tag before Edit button in `backend/apps/payments/templates/payments/payment_detail.html`
- [X] T011 [US1] Run linting (`ruff check backend/`) and fix any issues

**Checkpoint**: At this point, the Associate button should be functional and the association page accessible.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [X] T012 Run full test suite (`pytest backend/tests/test_payments_associate_button.py`) and confirm all tests pass
- [X] T013 Run `ruff check backend/` to confirm zero linting issues in new/modified code
- [X] T014 Move todo file `ai/features/todos/03-Button-access-reservations-payments.md` to `ai/features/done/` with appended session notes
- [X] T015 Save AI session markdown in `ai/sessions/` before PR

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup — T002 can run in parallel independently
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **Polish (Phase 4)**: Depends on User Story 1 being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependencies on other stories

### Within User Story 1

- Tests (T003-T007) MUST be written and FAIL before implementation (T008-T011)
- View GET handler before template rendering

### Parallel Opportunities

- T002 (i18n key) can run in parallel with T003-T007 (tests)
- T009 (new template) can run in parallel with T010 (edit existing template)

---

## Parallel Example: User Story 1

```bash
# Write all tests first:
Task: "T003 Test Associate button presence in backend/tests/test_payments_associate_button.py"
Task: "T004 Test button href in backend/tests/test_payments_associate_button.py"
Task: "T005 Test GET associate returns 200 in backend/tests/test_payments_associate_button.py"
Task: "T006 Test GET associate context in backend/tests/test_payments_associate_button.py"
Task: "T007 Test tab order in backend/tests/test_payments_associate_button.py"

# Implement in parallel:
Task: "T008 Add GET handler to PaymentAssociateView in backend/apps/payments/views.py"
Task: "T009 Create payment_associate.html template in backend/apps/payments/templates/payments/"
Task: "T010 Add Associate button to payment_detail.html in backend/apps/payments/templates/payments/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (i18n key)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test the Associate button independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP — this is the only story!)
3. Each task adds value without breaking previous work

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to the sole user story
- The user story is independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at checkpoint to validate story independently
