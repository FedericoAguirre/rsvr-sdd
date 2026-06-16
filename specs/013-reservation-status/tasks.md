# Tasks: Add Reservation Status

**Input**: Design documents from `/specs/013-reservation-status/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included. TDD is mandatory per Constitution — tests MUST be written first and fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app (Django)**: All paths under `backend/` at repository root
- Paths shown below follow the actual project structure from plan.md

## Phase 1: Setup

**Purpose**: Project initialization — no setup tasks needed, project infrastructure already exists.

- [X] T001 Verify Docker environment is running and tests pass before starting: `docker-compose exec web python -m pytest`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Status field on Reservation model — blocks ALL user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Add `status` CharField with choices (`reserved`, `used`, `unused`) and default `"reserved"` to Reservation model in `backend/apps/reservations/models.py`
- [X] T003 Create and apply migration: `docker-compose exec web python manage.py makemigrations reservations && docker-compose exec web python manage.py migrate`
- [X] T004 Add Spanish translations for status labels ("Reservado", "Usado", "No usado") in `backend/locale/es/LC_MESSAGES/django.po` and compile: `docker-compose exec web python manage.py compilemessages`

**Checkpoint**: Foundation ready — Reservation model has status field, migration applied, translations loaded

---

## Phase 3: User Story 1 - Mark Reservation as Used or Unused (Priority: P1) 🎯 MVP

**Goal**: Administrators and Operators can change a reservation's status on the detail view via a dedicated POST endpoint.

**Independent Test**: Navigate to `/reservations/<pk>/`, click "Usado" button, verify reservation status changes to "Usado" immediately.

### Tests for User Story 1 ⚠️ (TDD: Write FIRST, ensure FAIL before implementation)

- [X] T005 [US1] Write failing test for `reservation_change_status` view — POST to `/reservations/<pk>/status/` with `status=used` returns redirect and reservation status changes — in `backend/tests/test_reservations_list.py`
- [X] T006 [US1] Write failing test for status change edge cases (re-setting same status, invalid status value, unauthenticated user) in `backend/tests/test_reservations_list.py`

### Implementation for User Story 1

- [X] T007 [P] [US1] Add `reservation_change_status` view in `backend/apps/reservations/views.py` — POST-only, accepts `status`, validates input, redirects to detail with success/error message
- [X] T008 [P] [US1] Add URL pattern `path("<int:pk>/status/", views.reservation_change_status, name="reservation-change-status")` in `backend/apps/reservations/urls.py`
- [X] T009 [US1] Update `reservation_detail.html` template: display current status with Spanish label, add action buttons for each available status transition
- [X] T010 [US1] Make test T005 pass — verify status change flow works end-to-end
- [X] T011 [US1] Make test T006 pass — verify edge cases handled correctly

**Checkpoint**: At this point, User Story 1 should be fully functional — operators can change reservation status from the detail view

---

## Phase 4: User Story 2 - View Reservation Status in Listings (Priority: P1)

**Goal**: All reservation list views display the current status for every reservation with Spanish labels.

**Independent Test**: Navigate to `/reservations/list/?class_slot=<pk>&date=2026-06-15` and verify each row shows the correct status in Spanish.

### Tests for User Story 2 ⚠️ (TDD: Write FIRST, ensure FAIL before implementation)

- [X] T012 [US2] Write failing test for status column in list view — verify "Usado"/"No usado"/"Reservado" labels appear in `backend/tests/test_reservations_list.py`

### Implementation for User Story 2

- [X] T013 [P] [US2] Add status column to `backend/apps/reservations/templates/reservations/reservation_list.html`
- [X] T014 [P] [US2] Add status column to `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`
- [X] T015 [P] [US2] Add status column to `backend/apps/reservations/templates/reservations/reservation_list_pdf.html`
- [X] T016 [US2] Make test T012 pass — verify status displays correctly in all list views

**Checkpoint**: At this point, User Stories 1 AND 2 should both work — status visible everywhere, changeable from detail view

---

## Phase 5: User Story 3 - Filter Reservations by Status (Priority: P2)

**Goal**: Operators can filter the reservation list by status to see only reserved, used, or unused reservations.

**Independent Test**: Select "Usado" from status filter dropdown and verify only used reservations appear in the list.

### Tests for User Story 3 ⚠️ (TDD: Write FIRST, ensure FAIL before implementation)

- [X] T017 [US3] Write failing test for status filter — test filter by each status value, test clearing filter — in `backend/tests/test_reservations_list.py`

### Implementation for User Story 3

- [X] T018 [US3] Add optional `status` GET parameter to `reservation_list` view in `backend/apps/reservations/views.py` to filter by status
- [X] T019 [US3] Add status filter dropdown UI to `backend/apps/reservations/templates/reservations/reservation_list.html`
- [X] T020 [US3] Add status filter dropdown UI to `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`
- [X] T021 [US3] Make test T017 pass — verify filtering works end-to-end

**Checkpoint**: User Stories 1-3 are functional — status change, display, and filtering all work

---

## Phase 6: User Story 4 - Export Reservations with Status in PDF (Priority: P2)

**Goal**: PDF exports include the status column with correct Spanish labels.

**Independent Test**: Generate a PDF export and verify the status column values match each reservation's current status.

### Tests for User Story 4 ⚠️ (TDD: Write FIRST, ensure FAIL before implementation)

- [X] T022 [US4] Write failing test for status in PDF export — verify "Usado"/"No usado"/"Reservado" appear in PDF content — in `backend/tests/test_reservations_list.py`

### Implementation for User Story 4

- [X] T023 [US4] Make test T022 pass — status column already added to PDF template in T015, verify PDF renders status correctly

**Checkpoint**: All four user stories functional — status is displayed, changeable, filterable, and exported

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T024 [P] Add `status` to `list_display` in `backend/apps/reservations/admin.py`
- [X] T025 Run linting: `docker-compose exec web python -m ruff check backend/` and fix any issues
- [X] T026 Run full test suite: `docker-compose exec web python -m pytest` — verify 100% pass rate (SC-005)
- [X] T027 Move `ai/features/todos/02_add_reservation_status_to_reservation.md` to `ai/features/done/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Verify environment — can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Phase 2 completion
  - US1 (Phase 3) and US2 (Phase 4) are P1 — prioritize these
  - US3 (Phase 5) and US4 (Phase 6) are P2 — implement after P1
  - US4 is partially blocked by US2 (needs PDF template from T015)
- **Phase 7 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — No dependencies on other stories
- **US2 (P1)**: Can start after Phase 2 — No dependencies on other stories
- **US3 (P2)**: Can start after Phase 2 + US2 (needs list views with status)
- **US4 (P2)**: Can start after Phase 2 + US2 (needs PDF template with status column)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models/services before endpoints/templates
- Story complete before moving to next priority

### Parallel Opportunities

- T007 and T008 (US1) can run in parallel — different files, no dependencies
- T013, T014, T015 (US2) can run in parallel — different templates, no dependencies
- US1 and US2 can theoretically be started in parallel after Phase 2 (different concerns)

---

## Parallel Example: User Story 1

```bash
# Launch view and URL pattern together (T007 and T008):
Task: "Add reservation_change_status view in backend/apps/reservations/views.py"
Task: "Add URL pattern in backend/apps/reservations/urls.py"
```

## Parallel Example: User Story 2

```bash
# Launch all template updates together (T013, T014, T015):
Task: "Add status column to reservation_list.html"
Task: "Add status column to reservation_list_by_slot.html"
Task: "Add status column to reservation_list_pdf.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Verify environment
2. Complete Phase 2: Model + migration + translations
3. Complete Phase 3: User Story 1 (Mark as Used/Unused)
4. **STOP and VALIDATE**: Test US1 independently — operator can change status from detail view
5. Deploy/demo if ready

### Incremental Delivery

1. Phase 1 + Phase 2 → Foundation ready
2. Add US1 → Test independently → Deploy/Demo (MVP!)
3. Add US2 → Test independently → Deploy/Demo
4. Add US3 → Test independently → Deploy/Demo
5. Add US4 → Test independently → Deploy/Demo
6. Phase 7 Polish → Final

### Parallel Team Strategy

With multiple developers:

1. Complete Phase 1 + Phase 2 together
2. Once Foundational is done:
   - Developer A: US1 (Phase 3)
   - Developer B: US2 (Phase 4)
3. After P1 stories done:
   - Developer A: US3 (Phase 5)
   - Developer B: US4 (Phase 6)
4. Both converge on Phase 7 together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
