---

description: "Task list for implementing client class calendar ICS download"
---

# Tasks: Send Class Reservations Calendar to Client

**Input**: Design documents from `/specs/021-send-class-calendar/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/client-calendar-download.md

**Tests**: Tests are included per Constitution requirement (TDD mandatory, integration tests required for new library contract — `icalendar`).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/`, `backend/tests/`
- Paths reflect Django project structure under `backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [X] T001 Add `icalendar>=5.0` dependency in `backend/pyproject.toml`
- [X] T002 Install new dependency with `uv sync` in `backend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T003 Read existing `client_detail` view patterns in `backend/apps/clients/views.py` and `client_csv_template` HttpResponse pattern
- [X] T004 Read existing `client_detail.html` template structure in `backend/apps/clients/templates/clients/client_detail.html`

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Download ICS Calendar for a Client (Priority: P1) 🎯 MVP

**Goal**: Operator can navigate to the client detail page, select a date range, and download a valid ICS file containing all reservations in that range.

**Independent Test**: Navigate to client detail page, select start and end dates with reservations, click download, verify ICS file is received with correct filename and opens in a calendar application.

### Tests for User Story 1 ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T005 [P] [US1] Integration test for ICS download in `backend/tests/test_client_calendar.py` — authenticated user requests `clients/{pk}/calendar/?start_date=...&end_date=...` and receives 200 with `text/calendar` content type
- [X] T006 [P] [US1] Integration test verifying ICS content includes VEVENT with correct SUMMARY and DESCRIPTION fields in `backend/tests/test_client_calendar.py`
- [X] T007 [US1] Integration test verifying filename format `cal_*.ics` in `backend/tests/test_client_calendar.py`

### Implementation for User Story 1

- [X] T008 [US1] Add `calendar/` URL route in `backend/apps/clients/urls.py` — map `<int:pk>/calendar/` to `client_calendar` view with name `client-calendar`
- [X] T009 [US1] Implement `client_calendar` view in `backend/apps/clients/views.py` — parse `start_date`/`end_date` GET params, query reservations for client with `select_related("equipment", "class_slot")`, generate ICS response using `icalendar`, return as file download
- [X] T010 [US1] Implement snake_case filename generation: lowercase client full name, replace spaces with underscores, remove non-alphanumeric chars (except underscores), format as `cal_<name>_<start_YYYYMMDD>_<end_YYYYMMDD>.ics`
- [X] T011 [US1] Add date range form (start date + end date inputs) and "Download Calendar" button to `backend/apps/clients/templates/clients/client_detail.html` above the reservation history table
- [X] T012 [US1] Extract Spanish strings and run `makemessages` + `compilemessages` in `backend/` for all new UI text

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Handle Empty Date Range Gracefully (Priority: P2)

**Goal**: Operator sees a clear message when no reservations exist in the selected date range, instead of receiving an empty or broken file.

**Independent Test**: Select a date range with zero reservations for a client, verify a helpful message is shown and no file download occurs.

### Tests for User Story 2 ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T013 [US2] Integration test for empty range in `backend/tests/test_client_calendar.py` — request with date range having no reservations, verify no file download, verify HTML response contains empty-range message

### Implementation for User Story 2

- [X] T014 [US2] Add empty result check in `client_calendar` view in `backend/apps/clients/views.py` — if reservation count is zero after filter, render detail page with an info message instead of returning file
- [X] T015 [US2] Add empty-range message display area in `backend/apps/clients/templates/clients/client_detail.html` — Django messages pattern or inline conditional

**Checkpoint**: At this point, User Story 2 should work independently

---

## Phase 5: User Story 3 — Date Range Selection with Validation (Priority: P3)

**Goal**: Operator receives validation feedback when selecting an invalid date range (start date after end date).

**Independent Test**: Enter end date before start date and submit, verify an error message requests correction.

### Tests for User Story 3 ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T016 [US3] Integration test for date validation in `backend/tests/test_client_calendar.py` — request with `start_date` after `end_date`, verify error response and no file download

### Implementation for User Story 3

- [X] T017 [US3] Add date validation in `client_calendar` view in `backend/apps/clients/views.py` — if `start_date > end_date`, return error message without querying

**Checkpoint**: At this point, all user stories should be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and quality assurance

- [X] T018 [P] Add tests for special characters in client name (accents, apostrophes) in filename generation in `backend/tests/test_client_calendar.py`
- [X] T019 [P] Add test for unauthenticated access redirects to login in `backend/tests/test_client_calendar.py`
- [X] T020 [P] Add test for 404 when client PK doesn't exist in `backend/tests/test_client_calendar.py`
- [X] T021 Run full test suite with `uv run pytest` from `backend/` and verify all tests pass
- [X] T022 Run linting with `ruff check` from `backend/` and fix any issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories proceed sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 view existing (uses same `client_calendar` view)
- **User Story 3 (P3)**: Depends on US1 view existing (uses same `client_calendar` view)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- URL route before view
- View before template
- Template before translations

### Parallel Opportunities

- All test tasks marked [P] within a story can run in parallel
- T018, T019, T020 in Phase 6 can run in parallel
- Template changes and view changes are separated by task — implement view first, then template

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Integration test for ICS download in backend/tests/test_client_calendar.py"
Task: "Integration test verifying ICS content in backend/tests/test_client_calendar.py"

# Then implement sequentially:
Task: "Add calendar/ route in backend/apps/clients/urls.py"
Task: "Implement client_calendar view in backend/apps/clients/views.py"
Task: "Update client_detail.html template"
Task: "i18n translations"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (add icalendar)
2. Complete Phase 2: Foundational (read existing code)
3. Complete Phase 3: User Story 1 (core ICS download)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- US2 and US3 modify the same view (`client_calendar`) as US1 — implement as incremental additions
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
