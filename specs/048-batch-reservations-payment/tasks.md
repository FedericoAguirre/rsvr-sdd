# Tasks: Batch Reservations from Payment

**Input**: Design documents from `specs/048-batch-reservations-payment/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tasks include test tasks. Tests are written first (TDD).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/`, `backend/tests/`
- Paths shown follow the project's Django app structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Extend `PaymentCreateView.form_valid` to redirect with batch_modal param in `backend/apps/payments/views.py`
- [x] T002 [P] Add batch modal URL routes to `backend/apps/payments/urls.py`
- [x] T003 [P] Create `_batch_modal.html` template skeleton in `backend/apps/payments/templates/payments/_batch_modal.html`
- [x] T004 [P] Add batch modal trigger JS to `payment_detail.html` in `backend/apps/payments/templates/payments/payment_detail.html`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create `BatchReservationForm` with validation in `backend/apps/payments/forms.py`
- [x] T006 [P] Create `BatchCreateView` in `backend/apps/payments/views.py`
- [x] T007 [P] Create `BatchDataView` in `backend/apps/payments/views.py`
- [x] T008 [P] Add Spanish translations in `backend/locale/es/LC_MESSAGES/django.po`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 — Create Batch Reservations After Payment (Priority: P1) 🎯 MVP

**Goal**: Operator creates a payment, sees a batch modal, selects equipment/class slot/dates, and batch reservations are created and linked to the payment.

**Independent Test**: Create a payment with N=3 block classes, verify modal appears, select equipment + class slot + 3 DOW-matching dates, submit, verify 3 reservations exist linked to the payment via PaymentReservation.

### Tests for User Story 1 (TDD — write first, ensure FAIL before implementation)

- [x] T009 [P] [US1] Test batch modal appears after payment creation in `backend/tests/test_payments_batch.py`
- [x] T010 [P] [US1] Test batch modal context data in `backend/tests/test_payments_batch.py`
- [x] T011 [P] [US1] Test batch creation creates N reservations in `backend/tests/test_payments_batch.py`
- [x] T012 [P] [US1] Test batch redirects to payment detail in `backend/tests/test_payments_batch.py`
- [x] T013 [P] [US1] Test zero class_slot_count in `backend/tests/test_payments_batch.py`
- [x] T014 [P] [US1] Test partial failure on conflicts in `backend/tests/test_payments_batch.py`

### Implementation for User Story 1

- [x] T015 [US1] Implement `BatchReservationForm` in `backend/apps/payments/forms.py`
- [x] T016 [US1] Implement `BatchDataView` in `backend/apps/payments/views.py`
- [x] T017 [US1] Implement `PaymentCreateView` success handler in `backend/apps/payments/views.py`
- [x] T018 [US1] Implement `_batch_modal.html` template in `backend/apps/payments/templates/payments/_batch_modal.html`
- [x] T019 [US1] Implement batch modal trigger in `payment_detail.html` in `backend/apps/payments/templates/payments/payment_detail.html`
- [x] T020 [US1] Implement `BatchCreateView` POST handler in `backend/apps/payments/views.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Batch Size & Date Constraints (Priority: P1)

**Goal**: System enforces batch limits (≤20 reservations, 4-week date range, DOW matching, unique constraint) with clear user feedback.

**Independent Test**: Attempt to create batches exceeding each limit and verify the system prevents it with clear error messages.

### Tests for User Story 2 (TDD — write first, ensure FAIL before implementation)

- [x] T021 [P] [US2] Test exceeding 20 reservations in `backend/tests/test_payments_batch.py`
- [x] T022 [P] [US2] Test dates outside 4-week range in `backend/tests/test_payments_batch.py`
- [x] T023 [P] [US2] Test fewer dates than block count in `backend/tests/test_payments_batch.py`
- [x] T024 [P] [US2] Test DOW mismatch in `backend/tests/test_payments_batch.py`
- [x] T025 [P] [US2] Test partial conflict display in `backend/tests/test_payments_batch.py`

### Implementation for User Story 2

- [x] T026 [US2] Add max-20 validation to `BatchReservationForm` in `backend/apps/payments/forms.py`
- [x] T027 [US2] Add 4-week date range validation to `BatchReservationForm` in `backend/apps/payments/forms.py`
- [x] T028 [US2] Add exactly-N-dates validation to `BatchReservationForm` in `backend/apps/payments/forms.py`
- [x] T029 [US2] Add DOW matching filter to `BatchDataView` in `backend/apps/payments/views.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T030 [P] Update `payment_detail.html` with batch modal and associated reservations in `backend/apps/payments/templates/payments/payment_detail.html`
- [x] T031 [P] Compile Django i18n message files for Spanish translations
- [x] T032 [P] Date formatting handled in JS (Spanish day abbreviations) in `payment_detail.html`
- [x] T033 Run test suite — all 11 batch tests + 65 existing tests pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+4)**: All depend on Foundational phase completion
  - US1 and US2 are tightly coupled (constraints validated during batch creation); implement together
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on T001–T008 (Setup + Foundational)
- **User Story 2 (P1)**: Depends on T001–T008; implemented alongside US1 (shared form/view)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Form before view
- View before template
- Template before integration test

### Parallel Opportunities

- T002, T003, T004 can run in parallel (Setup)
- T006, T007, T008 can run in parallel (Foundational)
- All US1/2 test tasks (T009–T014, T021–T025) can run in parallel
- T030, T031, T032 can run in parallel (Polish)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test batch modal appears after payment creation in backend/tests/test_payments_batch.py"
Task: "Test batch modal context data in backend/tests/test_payments_batch.py"
Task: "Test batch creation creates N reservations in backend/tests/test_payments_batch.py"

# Launch form + view implementation together:
Task: "Implement BatchReservationForm in backend/apps/payments/forms.py"
Task: "Implement BatchDataView in backend/apps/payments/views.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 — both P1)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3+4: User Stories 1 + 2 (implement together)
4. **STOP and VALIDATE**: Test batch creation flow end-to-end
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Modal skeleton works
2. Add form validation → Constraints enforced
3. Add views + template → Full batch creation flow
4. Compile translations → Spanish labels ready

### Environment Reference

- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Run tests**: `docker compose exec web pytest -v`
- **Run specific tests**: `docker compose exec web pytest backend/tests/test_payments_batch.py -v`
- **Compile translations**: `docker compose exec web uv run manage.py compilemessages`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
