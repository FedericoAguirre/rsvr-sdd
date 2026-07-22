# Tasks: Calendar Downloading in Reservations Page

**Input**: Design documents from `specs/050-calendar-downloading-reservations/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Django backend**: `backend/apps/`, `backend/tests/`, `backend/utils/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and context setup

- [X] T001 Fetch current icalendar docs via Context7 MCP (Principle V compliance) before writing any ICS generation code
- [X] T002 [P] Extract shared ICS utility from `backend/apps/clients/views.py::_generate_ics` into `backend/utils/ical.py::generate_ics`
- [X] T003 [P] Create tests for shared utility in `backend/tests/test_ical_utils.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Refactor existing apps to use the shared utility before adding the new feature

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Refactor `backend/apps/clients/views.py` to import and use `generate_ics` from `backend/utils/ical.py`
- [X] T005 Refactor `backend/apps/payments/views.py` to import and use `generate_ics` from `backend/utils/ical.py` (pass `extra_fields_fn` for the `\nPago:` line)

**Checkpoint**: Foundation ready — shared utility exists, both existing apps use it, no regression

---

## Phase 3: User Story 1 — Download Calendar from Reservations List (Priority: P1) 🎯 MVP

**Goal**: Operator filters reservations by date range and downloads an ICS file with payment identifiers in each event description.

**Independent Test**: Visit the reservations page, set a date range, click "Download Calendar", verify the ICS file includes all expected reservations with client name, class slot, date, equipment, and payment identifier in each event description.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T006 [P] [US1] Test ICS generation for reservations with payment in `backend/tests/test_reservations_calendar.py`
- [X] T007 [P] [US1] Test ICS filename format in `backend/tests/test_reservations_calendar.py`
- [X] T008 [P] [US1] Test empty date range handling in `backend/tests/test_reservations_calendar.py`
- [X] T009 [P] [US1] Test missing date range parameters in `backend/tests/test_reservations_calendar.py`

### Implementation for User Story 1

- [X] T010 [US1] Add `reservation_calendar` view in `backend/apps/reservations/views.py` — accepts `start_date`/`end_date` query params, filters reservations, calls `generate_ics` with `extra_fields_fn` that includes payment identifier
- [X] T011 [US1] Add `calendar/` URL route in `backend/apps/reservations/urls.py` pointing to `reservation_calendar`
- [X] T012 [US1] Add "Descargar calendario" button and date range form to `backend/apps/reservations/templates/reservations/reservation_list.html`

**Checkpoint**: US1 should be fully functional — reservations calendar download works with payment identifiers

---

## Phase 4: User Story 2 — Handle Unassociated Reservations (Priority: P2)

**Goal**: Reservations not linked to any payment still appear in the calendar with "Reservación sin asociar" as the payment identifier.

**Independent Test**: Create reservations without payment association, download the calendar, verify the ICS includes them with "Reservación sin asociar" as the payment identifier.

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US2] Test unassociated reservation shows "Reservación sin asociar" in `backend/tests/test_reservations_calendar.py`
- [X] T014 [P] [US2] Test mixed reservations (some associated, some not) in `backend/tests/test_reservations_calendar.py`

### Implementation for User Story 2

- [X] T015 [US2] Update `extra_fields_fn` in `reservation_calendar` view to use `payment.identifier` if payment exists, else "Reservación sin asociar"

**Checkpoint**: US2 should work — unassociated reservations show correct fallback text

---

## Phase 5: User Story 3 — Multiple Payments in Date Range (Priority: P2)

**Goal**: Date ranges spanning multiple payments include all reservations in a single ICS file with correct per-event payment identifiers.

**Independent Test**: Create reservations across two different payments within the same date range, download the calendar, verify all appear with correct payment identifiers.

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T016 [P] [US3] Test multiple payments in same date range in `backend/tests/test_reservations_calendar.py`
- [X] T017 [P] [US3] Test each event has correct payment identifier in `backend/tests/test_reservations_calendar.py`

### Implementation for User Story 3

- [X] T018 [US3] Verify reservation query in `reservation_calendar` view includes all reservations across all payments (no per-payment filtering)

**Checkpoint**: All three stories should work — reservations from any payment in the date range are included

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: i18n, cleanup, and final verification

- [X] T019 [P] Extract all new user-visible strings with `django-admin makemessages -l es`
- [X] T020 [P] Translate new strings in `backend/locale/es/LC_MESSAGES/django.po`
- [X] T021 Run `django-admin compilemessages` to compile translations
- [X] T022 Remove any remaining dead code (old `_generate_ics` references after refactoring)
- [X] T023 Run full test suite: `docker compose exec web uv run pytest`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational
  - US2 and US3 are edge cases within the same view as US1 — they modify the same files
  - Recommended to implement sequentially: US1 → US2 → US3
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — No dependencies on other stories
- **US2 (P2)**: Can start after Foundational — Tests and implementation touch the same files as US1; best done sequentially
- **US3 (P2)**: Can start after Foundational — Same view as US1/US2; minimal additional code

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Test → Implement → Verify cycle per story

### Parallel Opportunities

- T002 and T003 in Phase 1 can run in parallel
- T004 and T005 in Phase 2 can run in parallel
- All tests for a given user story marked [P] can run in parallel
- T019 and T020 in Phase 6 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test ICS generation for reservations with payment in backend/tests/test_reservations_calendar.py"
Task: "Test ICS filename format in backend/tests/test_reservations_calendar.py"
Task: "Test empty date range handling in backend/tests/test_reservations_calendar.py"
Task: "Test missing date range parameters in backend/tests/test_reservations_calendar.py"

# Implementation is sequential (view depends on route, route depends on template):
Task: "Add reservation_calendar view in backend/apps/reservations/views.py"
Task: "Add calendar/ URL route in backend/apps/reservations/urls.py"
Task: "Add download button and date form to backend/apps/reservations/templates/reservations/reservation_list.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (shared utility + Context7 docs)
2. Complete Phase 2: Foundational (refactor existing apps)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test US1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Shared utility ready, existing apps refactored
2. Add US1 → Reservations calendar download with payment IDs → Deploy/Demo (MVP!)
3. Add US2 → Unassociated reservation handling → Deploy/Demo
4. Add US3 → Multi-payment date range support → Deploy/Demo

### Environment Reference

- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Run tests**: `docker compose exec web uv run pytest`
- **Run specific tests**: `docker compose exec web uv run pytest backend/tests/test_reservations_calendar.py -v`
- **Install packages**: `docker compose run --rm web uv add <package>`
- **i18n extract**: `docker compose exec web uv run manage.py makemessages -l es`
- **i18n compile**: `docker compose exec web uv run manage.py compilemessages`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All user-visible strings MUST use i18n (Principle III — NON-NEGOTIABLE)
- Context7 MCP MUST be used for icalendar docs before writing ICS code (Principle V)
