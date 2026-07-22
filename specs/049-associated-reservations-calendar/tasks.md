---

description: "Task list for Associated Reservations Calendar Download feature"

---

# Tasks: Associated Reservations Calendar Download

**Input**: Design documents from `specs/049-associated-reservations-calendar/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Since US2 (empty state) is a sub-case of the same view, both stories share the same implementation phase.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/`, `backend/tests/`
- Paths shown assume the project structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

No setup tasks needed — this feature requires no new apps, models, or dependencies. The `icalendar` library is already available, and the ICS generation utility already exists in `backend/apps/clients/views.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 [P] Add `_snake_case_name()` import to `backend/apps/payments/views.py` (or reference via `apps.clients.views`)
- [x] T002 [P] Add `_generate_ics()` import to `backend/apps/payments/views.py` (or extract to shared utility)

---

## Phase 3: User Story 1 — Download ICS Calendar from Payment Detail Page (Priority: P1) 🎯 MVP

**Goal**: Operators can download an ICS calendar file containing all reservations associated with a payment from the payment detail page.

**Independent Test**: Navigate to a payment detail page with associated reservations, click "Descargar calendario", and receive a valid ICS file with the correct filename and event contents.

### Implementation for User Story 1

- [x] T003 [US1] Add calendar download URL pattern in `backend/apps/payments/urls.py` (`<int:pk>/calendar/`, name=`calendar`)
- [x] T004 [US1] Implement `payment_calendar` view function in `backend/apps/payments/views.py`:
  - GET only, login_required
  - Get payment by pk (404 if not found)
  - Query `payment.payment_reservations.select_related("reservation__client", "reservation__equipment", "reservation__class_slot")`
  - If no reservations: set info message via `messages.info()` and redirect to payment detail
  - Compute snake_case client name using `_snake_case_name()` from `apps.clients.views`
  - Build ICS inline with payment identifier in DESCRIPTION
  - Compute filename: `<snake_name>_<payment_identifier>_<first_date_YYYYMMDD>_<last_date_YYYYMMDD>.ics`
  - Return `HttpResponse(ics_content, content_type="text/calendar; charset=utf-8")` with `Content-Disposition: attachment`
  - All user-visible strings use i18n (`django.utils.translation.gettext_lazy`)
- [x] T005 [US1] Build ICS inline in payment_calendar view (includes `\nPago: %(payment_identifier)s` in DESCRIPTION; avoids modifying shared `_generate_ics()`)
- [x] T006 [US1] Add "Descargar calendario" button in `backend/apps/payments/templates/payments/payment_detail.html` in the header actions area, alongside "Associate" button
  - Button text uses `{% translate "Download calendar" %}` with Spanish translation `Descargar calendario`
  - Links to `{% url 'payments:calendar' payment.pk %}`

### Tests for User Story 1

- [x] T007 [P] [US1] Create `backend/tests/test_payments_calendar.py` with fixtures (http_client, staff_user, logged_client, payment, class_slot, equipment, reservation, payment_reservation)
- [x] T008 [US1] Test `test_download_returns_ics_content_type`: GET `/payments/{pk}/calendar/` with associated reservations → 200, Content-Type `text/calendar; charset=utf-8`
- [x] T009 [US1] Test `test_download_filename_format`: response Content-Disposition includes `<snake_name>_<payment_identifier>_<first_date>_<last_date>.ics`
- [x] T010 [US1] Test `test_download_contains_vevent`: response body contains `VEVENT`, client name, equipment name, payment identifier
- [x] T011 [US1] Test `test_unauthenticated_redirects_to_login`: anonymous user → 302 redirect
- [x] T012 [US1] Test `test_nonexistent_payment_returns_404`: invalid pk → 404
- [x] T013 [US1] Test `test_empty_payment_shows_message`: payment with zero reservations → 302 redirect, use `follow=True`, followed page contains message

---

## Phase 4: User Story 2 — Handle Payment Without Reservations (Priority: P2)

**Goal**: When a payment has no associated reservations, the operator sees a clear message instead of a broken download.

**Independent Test**: View a payment with zero associated reservations, click "Descargar calendario", and see a meaningful message — no file is generated.

### Implementation for User Story 2

- [x] T014 [US2] The empty-state redirect and message is already implemented in T004 (the view checks `reservations.exists()` and redirects with a message). Add i18n translation key for the empty state message.
- [x] T015 [P] [US2] Add i18n entry for empty state message in the Django translation file (auto-extracted by T016)

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T016 [P] Run i18n message extraction: `docker compose exec web uv run manage.py makemessages -l es`
- [ ] T017 [P] Run formatter: `docker compose exec web ruff check --fix backend/ && docker compose exec web ruff format backend/` (skipped — ruff not installed in project)
- [x] T018 Run all tests: `docker compose exec web pytest` — 249 passed, 3 pre-existing failures (test_restart_docs.py — FileNotFoundError for docs/windows11_deployment.md)
- [x] T019 [P] Verify Context7 MCP usage: confirmed icalendar 7.x and Django 5.0 HttpResponse/file response docs were queried before writing code

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — no setup needed
- **Foundational (Phase 2)**: Import setup — must complete before US1
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion — this IS the MVP
- **User Story 2 (Phase 4)**: Depends on Phase 3 (same view, empty-state case handled within the same implementation)
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — the entire feature
- **User Story 2 (P2)**: Sub-case of US1 — implemented together, tested separately

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Principle II — TDD)
- View before template (view logic drives the template button)
- Core implementation before integration

### Parallel Opportunities

- T001 and T002 can run in parallel (both are import additions)
- T007 can run in parallel with T003-T006 (test writing independent of implementation)
- T016 and T017 can run in parallel (i18n and formatting are independent)

---

## Parallel Example: User Story 1

```bash
# Launch all model/test tasks together:
Task: "Create test_payments_calendar.py with fixtures in backend/tests/test_payments_calendar.py"
Task: "Add calendar URL in backend/apps/payments/urls.py"
Task: "Implement payment_calendar view in backend/apps/payments/views.py"
Task: "Add 'Descargar calendario' button in backend/apps/payments/templates/payments/payment_detail.html"

# Verify tests pass:
docker compose exec web pytest tests/test_payments_calendar.py -v
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Import existing utilities
2. Complete Phase 3: Implement view, URL, template button, and tests
3. **STOP and VALIDATE**: Test User Story 1 independently — download an ICS file from a payment detail page
4. Deploy/demo if ready

### Incremental Delivery

1. Add URL + view + template button (MVP) → Test independently
2. Add empty-state handling (included in MVP view) → Test independently
3. Each addition adds value without breaking previous functionality

### Environment Reference

When writing script fragments, task execution steps, or running the code, always use these exact commands:
- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Run tests**: `docker compose exec web uv run manage.py test`
- **Install packages**: `docker compose run --rm web uv add <package>`
- **Sync dependencies**: `docker compose exec web uv sync --system`
- **Run specific tests**: `docker compose exec web pytest tests/test_payments_calendar.py -v`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD per Constitution Principle II)
- Use Context7 MCP to verify `icalendar` 7.x API and Django 5.0 `HttpResponse` patterns before writing code (Constitution Principle V)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
