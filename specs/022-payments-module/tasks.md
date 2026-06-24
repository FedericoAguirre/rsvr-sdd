---

description: "Task list for payments module implementation"

---

# Tasks: Payments Module

**Input**: Design documents from `/specs/022-payments-module/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: The constitution mandates TDD (Red-Green-Refactor). Tests must be written first and fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root
- Django app: `backend/apps/payments/`
- Tests: `backend/tests/test_payments.py`
- Templates: `backend/apps/payments/templates/payments/`
- Config: `backend/config/`, `backend/templates/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the payments Django app and register it in the project

- [x] T001 [P] Create payments app structure with `python manage.py startapp payments apps/payments` and add `apps.py` with Spanish verbose_name
- [x] T002 Register `apps.payments` in `INSTALLED_APPS` in `backend/config/settings.py`
- [x] T003 Add Chart.js 4.x CDN script tag to `backend/templates/base.html`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core model and config that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Payment model with all fields (client, amount, payment_type, payment_identifier, date, class_slot_count, reference, evidence, notes, is_deleted, deleted_at, created_at, updated_at, created_by, updated_by) in `backend/apps/payments/models.py`
- [x] T005 Implement `Payment.save()` method for payment identifier auto-generation (format: type acronym + YYYYMMDD + client initials + 3-digit consecutive counter per-day per-type) in `backend/apps/payments/models.py`
- [x] T006 Create and run initial migration with `python manage.py makemigrations payments && python manage.py migrate`
- [x] T007 Configure `backend/apps/payments/admin.py` with Payment model registration
- [x] T008 Create `backend/apps/payments/urls.py` with all route definitions from contracts
- [x] T009 Include payments URLs in `backend/config/urls.py` under `path("payments/", include("apps.payments.urls"))`
- [x] T010 Add "Pagos" navigation link to `backend/templates/base.html`
- [x] T011 Set up Django Groups "Operators" and "Administrators" for role-based access (management command in `backend/apps/payments/management/commands/setup_groups.py`)
- [x] T012 Create `backend/apps/payments/apps.py` with `verbose_name = "Pagos"` following existing app conventions

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Register a Client Payment (Priority: P1) 🎯 MVP

**Goal**: Operators can register a client payment with all required fields, optional evidence, reference, and notes. Payments use auto-generated identifiers. Limited edit (reference/notes/evidence) and soft-delete are supported.

**Independent Test**: Can be fully tested by creating a new payment record and verifying all entered data is saved and visible. Delivers the ability to digitize payment records.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [P] [US1] Write unit test for Payment model creation with valid data in `backend/tests/test_payments.py`
- [x] T014 [P] [US1] Write unit test for Payment identifier auto-generation format and uniqueness in `backend/tests/test_payments.py`
- [x] T015 [P] [US1] Write unit test for Payment validation (required fields, positive amount, class_slot_count ≥ 1) in `backend/tests/test_payments.py`
- [x] T016 [P] [US1] Write unit test for Payment optional fields (reference, evidence, notes) in `backend/tests/test_payments.py`
- [x] T017 [P] [US1] Write unit test for limited edit (only reference/notes/evidence can change) in `backend/tests/test_payments.py`
- [x] T018 [P] [US1] Write unit test for Payment soft-delete in `backend/tests/test_payments.py`
- [x] T019 [P] [US1] Write unit test for PaymentForm validation (missing required, invalid data, evidence size/type) in `backend/tests/test_payments.py`

### Implementation for User Story 1

- [x] T020 [US1] Implement PaymentCreateView (GET + POST) in `backend/apps/payments/views.py`
- [x] T021 [US1] Create PaymentForm in `backend/apps/payments/forms.py` with all fields, optional evidence validation (5MB, JPEG/PNG), and custom identifier override
- [x] T022 [US1] Create payment_form.html template extending base.html with `{% load i18n %}` at `backend/apps/payments/templates/payments/payment_form.html`
- [x] T023 [US1] Implement PaymentDetailView in `backend/apps/payments/views.py`
- [x] T024 [US1] Create payment_detail.html template at `backend/apps/payments/templates/payments/payment_detail.html`
- [x] T025 [US1] Implement PaymentUpdateView (limited to reference, notes, evidence fields) in `backend/apps/payments/views.py`
- [x] T026 [US1] Implement PaymentDeleteView (soft-delete) in `backend/apps/payments/views.py`
- [x] T027 [US1] Create payment_confirm_delete.html template at `backend/apps/payments/templates/payments/payment_confirm_delete.html`
- [x] T028 [US1] Add audit logging for payment creation, edit, and soft-delete operations in `backend/apps/payments/views.py`
- [x] T029 [US1] Translate all user-facing strings to Spanish using Django i18n

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Client Payment History (Priority: P2)

**Goal**: Operators can view a client's payment history sorted by descending date, paginated at 5 per page. Empty state handled gracefully.

**Independent Test**: Can be fully tested by navigating to a client's payment history and verifying the list shows payments ordered by date with correct pagination.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T030 [P] [US2] Write integration test for PaymentListView with pagination (5 per page, descending date) in `backend/tests/test_payments.py`
- [ ] T031 [P] [US2] Write test for empty payment history (no payments for client) in `backend/tests/test_payments.py`
- [ ] T032 [P] [US2] Write test for client filter in payment list in `backend/tests/test_payments.py`

### Implementation for User Story 2

- [ ] T033 [US2] Implement PaymentListView (paginated, client filter via URL param) in `backend/apps/payments/views.py`
- [ ] T034 [US2] Implement client_history view (filtered by client_id, 5 per page, descending date) in `backend/apps/payments/views.py`
- [ ] T035 [US2] Create payment_list.html template with pagination controls and empty state message at `backend/apps/payments/templates/payments/payment_list.html`
- [ ] T036 [US2] Create template filters/tags in `backend/apps/payments/templatetags/payment_extras.py` for payment type labels and status display
- [ ] T037 [US2] Translate all user-facing strings to Spanish using Django i18n

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Associate Payment with Reservations (Priority: P3)

**Goal**: Operators can link a payment to N reservations (N ≤ class_slot_count) in a two-step flow from the New Reservations page or from payment detail.

**Independent Test**: Can be fully tested by creating a payment and associating it with N reservations.

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T038 [P] [US3] Write unit test for PaymentReservation model in `backend/tests/test_payments.py`
- [ ] T039 [P] [US3] Write integration test for Payment-Reservation association (success case) in `backend/tests/test_payments.py`
- [ ] T040 [P] [US3] Write integration test for class_slot_count limit enforcement in `backend/tests/test_payments.py`
- [ ] T041 [P] [US3] Write integration test for same-client validation in `backend/tests/test_payments.py`
- [ ] T042 [P] [US3] Write integration test for preventing double-linking a reservation in `backend/tests/test_payments.py`

### Implementation for User Story 3

- [ ] T043 [US3] Create PaymentReservation junction model in `backend/apps/payments/models.py`
- [ ] T044 [US3] Create and run migration for PaymentReservation model
- [ ] T045 [US3] Implement association view (POST /payments/{id}/associate/) in `backend/apps/payments/views.py`
- [ ] T046 [US3] Implement create_from_reservation view (GET/POST) for New Reservations page integration in `backend/apps/payments/views.py`
- [ ] T047 [US3] Add associated reservations display to payment_detail.html template
- [ ] T048 [US3] Add payment info to reservation detail view (read-only) in the existing reservations app
- [ ] T049 [US3] Translate all user-facing strings to Spanish using Django i18n

**Checkpoint**: All user stories 1-3 should now be independently functional

---

## Phase 6: User Story 4 - View Payment Reports (Priority: P4)

**Goal**: Administrators can view payment summaries grouped by day/week/month/custom date range with Chart.js visualizations.

**Independent Test**: Can be fully tested by selecting different date ranges and payment type groupings and verifying aggregated totals.

### Tests for User Story 4 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T050 [P] [US4] Write integration test for report aggregation (by day, week, month, range) in `backend/tests/test_payments.py`
- [ ] T051 [P] [US4] Write integration test for payment type grouping in reports in `backend/tests/test_payments.py`
- [ ] T052 [P] [US4] Write integration test for admin permission enforcement (operator sees access denied) in `backend/tests/test_payments.py`

### Implementation for User Story 4

- [ ] T053 [US4] Implement PaymentReportView (admin-only, date range filter, grouping) in `backend/apps/payments/views.py`
- [ ] T054 [US4] Create payment_reports.html template with Chart.js (bar chart for totals, pie chart for payment type distribution) at `backend/apps/payments/templates/payments/payment_reports.html`
- [ ] T055 [US4] Pass serialized chart data via Django `json_script` template tag for Chart.js consumption in payment_reports.html
- [ ] T056 [US4] Apply `@user_passes_test` or `@permission_required` decorator to report views for admin-only access
- [ ] T057 [US4] Translate all user-facing strings to Spanish using Django i18n

**Checkpoint**: All user stories are now independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T058 [P] Run `ruff check backend/` and fix all linting issues
- [ ] T059 Run `python manage.py check` and verify no warnings
- [ ] T060 Run full test suite with `pytest backend/tests/ -v` and confirm all tests pass
- [ ] T061 [P] Add evidence image handling (file cleanup on soft-delete, storage configuration for production via django-storages)
- [ ] T062 [P] Add structured logging for payment operations (create, edit, delete, associate) in `backend/apps/payments/views.py`
- [ ] T063 Save AI session file in `ai/sessions/` following naming convention: `{model}-payments-module-{timestamp}.md`
- [ ] T064 Move `ai/features/todos/08_add_payments_module.md` to `ai/features/done/` if this originated from a todos file

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (P1) must be completed before US2-4
  - US2 (P2) can run after US1
  - US3 (P3) can run after US1 (depends on Payment model, independent of US2)
  - US4 (P4) can run after US1 (depends on Payment model, independent of US2-3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1) — Register Payment**: Dependencies — Foundational (Phase 2). No dependencies on other stories.
- **US2 (P2) — View Payment History**: Dependencies — Foundational (Phase 2), US1 (needs payments to exist to view history)
- **US3 (P3) — Associate with Reservations**: Dependencies — Foundational (Phase 2), US1 (needs payments to exist to associate). Independent of US2.
- **US4 (P4) — Payment Reports**: Dependencies — Foundational (Phase 2), US1 (needs payments to aggregate). Independent of US2 and US3.

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services (tests depend on models)
- Views before templates (templates need view context)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Tests within a user story marked [P] can run in parallel
- US3 and US4 can be developed in parallel after US1 completes
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (must fail before implementation):
Task: "Write unit test for Payment model creation with valid data in backend/tests/test_payments.py"
Task: "Write unit test for Payment identifier auto-generation format and uniqueness in backend/tests/test_payments.py"
Task: "Write unit test for Payment validation in backend/tests/test_payments.py"
Task: "Write unit test for Payment optional fields in backend/tests/test_payments.py"
Task: "Write unit test for limited edit in backend/tests/test_payments.py"
Task: "Write unit test for Payment soft-delete in backend/tests/test_payments.py"
Task: "Write unit test for PaymentForm validation in backend/tests/test_payments.py"

# After tests fail, implement views and templates:
Task: "Implement PaymentCreateView, PaymentDetailView, PaymentUpdateView, PaymentDeleteView"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (register payments, edit, delete)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Register Payment) → Test independently → Deploy/Demo (MVP!)
3. Add US2 (View History) → Test independently → Deploy/Demo
4. Add US3 (Associate Reservations) → Test independently → Deploy/Demo
5. Add US4 (Payment Reports) → Test independently → Deploy/Demo

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP — critical path)
   - Developer B: Write tests for US1 (coordinated with Developer A)
3. After US1 completes:
   - Developer A: User Story 2
   - Developer B: User Story 3 (or US4)
4. Polish phase is a team effort

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD is required by constitution — verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All user-facing UI strings must use Django i18n for Spanish translation
- Evidence images: 5MB limit, JPEG/PNG only, validated at form level
- Payment identifier auto-generation: per-day per-type counter starting at 001
