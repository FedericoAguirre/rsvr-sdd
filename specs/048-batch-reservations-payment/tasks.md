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

- [ ] T001 Extend `PaymentCreateView.form_valid` to return JSON response with payment ID for HTMX modal trigger in `backend/apps/payments/views.py`
- [ ] T002 [P] Add batch modal URL routes to `backend/apps/payments/urls.py`
- [ ] T003 [P] Create `_batch_modal.html` template skeleton in `backend/apps/payments/templates/payments/_batch_modal.html`
- [ ] T004 [P] Add batch modal trigger JS to `payment_form.html` in `backend/apps/payments/templates/payments/payment_form.html`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create `BatchReservationForm` with validation (equipment in service, class slot active, dates within range, DOW matching, exactly N dates, ≤20, no duplicates) in `backend/apps/payments/forms.py`
- [ ] T006 [P] Create `BatchCreateView` that handles batch submission (receives payment_id, equipment_id, class_slot_id, dates list; validates via form; creates Reservation + PaymentReservation in transaction with partial failure) in `backend/apps/payments/views.py`
- [ ] T007 [P] Create `BatchDataView` that returns JSON context for modal (available dates range, equipment list filtered to "in service", active class slots) in `backend/apps/payments/views.py`
- [ ] T008 [P] Add Spanish translations for new batch modal labels and messages in `backend/locale/es/LC_MESSAGES/django.po`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 — Create Batch Reservations After Payment (Priority: P1) 🎯 MVP

**Goal**: Operator creates a payment, sees a batch modal, selects equipment/class slot/dates, and batch reservations are created and linked to the payment.

**Independent Test**: Create a payment with N=3 block classes, verify modal appears, select equipment + class slot + 3 DOW-matching dates, submit, verify 3 reservations exist linked to the payment via PaymentReservation.

### Tests for User Story 1 (TDD — write first, ensure FAIL before implementation)

- [ ] T009 [P] [US1] Test batch modal appears after payment creation in `backend/tests/test_payments_batch.py`
- [ ] T010 [P] [US1] Test batch modal context data returns correct equipment/class_slot/date range in `backend/tests/test_payments_batch.py`
- [ ] T011 [P] [US1] Test batch creation creates N reservations linked to payment in `backend/tests/test_payments_batch.py`
- [ ] T012 [P] [US1] Test batch redirects to payment detail showing associated reservations in `backend/tests/test_payments_batch.py`
- [ ] T013 [P] [US1] Test batch with zero class_slot_count does not show modal in `backend/tests/test_payments_batch.py`
- [ ] T014 [P] [US1] Test partial failure on unique constraint conflicts in `backend/tests/test_payments_batch.py`

### Implementation for User Story 1

- [ ] T015 [US1] Implement `BatchReservationForm` validation logic in `backend/apps/payments/forms.py`
- [ ] T016 [US1] Implement `BatchDataView` GET endpoint returning filtered equipment, active class slots, and date range in `backend/apps/payments/views.py`
- [ ] T017 [US1] Implement `PaymentCreateView` success handler: save payment, return JSON with payment_id and modal trigger in `backend/apps/payments/views.py`
- [ ] T018 [US1] Implement `_batch_modal.html` template with calendar day selector (DOW-filtered), equipment dropdown, class slot dropdown, date counter (N/max), and submit/close buttons in `backend/apps/payments/templates/payments/_batch_modal.html`
- [ ] T019 [US1] Implement modal trigger in `payment_form.html` — after successful payment submission, fetch batch data and open modal via JS/HTMX in `backend/apps/payments/templates/payments/payment_form.html`
- [ ] T020 [US1] Implement `BatchCreateView` POST handler: validate form, create Reservation + PaymentReservation in transaction, handle partial failure in `backend/apps/payments/views.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Batch Size & Date Constraints (Priority: P1)

**Goal**: System enforces batch limits (≤20 reservations, 4-week date range, DOW matching, unique constraint) with clear user feedback.

**Independent Test**: Attempt to create batches exceeding each limit and verify the system prevents it with clear error messages.

### Tests for User Story 2 (TDD — write first, ensure FAIL before implementation)

- [ ] T021 [P] [US2] Test exceeding 20 reservations shows warning in `backend/tests/test_payments_batch.py`
- [ ] T022 [P] [US2] Test selecting dates outside 4-week range is prevented in `backend/tests/test_payments_batch.py`
- [ ] T023 [P] [US2] Test selecting fewer dates than block class count is prevented in `backend/tests/test_payments_batch.py`
- [ ] T024 [P] [US2] Test DOW mismatch prevents date selection in `backend/tests/test_payments_batch.py`
- [ ] T025 [P] [US2] Test partial conflict display in payment detail page in `backend/tests/test_payments_batch.py`

### Implementation for User Story 2

- [ ] T026 [US2] Add max-20 validation to `BatchReservationForm.clean_dates` in `backend/apps/payments/forms.py`
- [ ] T027 [US2] Add 4-week date range validation to `BatchReservationForm.clean_dates` in `backend/apps/payments/forms.py`
- [ ] T028 [US2] Add exactly-N-dates validation (must equal block class count) to `BatchReservationForm.clean_dates` in `backend/apps/payments/forms.py`
- [ ] T029 [US2] Add DOW matching filter to `BatchDataView` date range — only show dates matching selected class slot's weekday in `backend/apps/payments/views.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T030 [P] Update `payment_detail.html` to show batch-created reservations with the same display as associated reservations in `backend/apps/payments/templates/payments/payment_detail.html`
- [ ] T031 [P] Compile and apply Django i18n message files for Spanish translations in `backend/locale/es/LC_MESSAGES/`
- [ ] T032 [P] Add date formatting helper (Spanish day abbreviations: L, M, X, J, V, S, D) in `backend/apps/payments/templatetags/payment_extras.py`
- [ ] T033 Run quickstart.md validation — manual test flow

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
