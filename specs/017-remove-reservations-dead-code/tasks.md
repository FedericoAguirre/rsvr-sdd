# Tasks: Remove Reservations Dead Code

**Input**: Design documents from `specs/017-remove-reservations-dead-code/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not requested by spec. Verification is via existing test suite (retained tests must pass).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root (Django monolith)
- Tests: `backend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Understand current codebase state and verify prerequisites

- [X] T001 Review current URL configuration in `backend/apps/reservations/urls.py` and verify routes
- [X] T002 Review current view logic in `backend/apps/reservations/views.py` to confirm which code is dead
- [X] T003 Verify existing test suite passes with `pytest backend/tests/test_reservations_list.py -v`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure the ghost migration artifact is cleaned up first to avoid interference

**⚠️ CRITICAL**: The orphaned `.pyc` file must be removed before creating the new migration to prevent Django from conflating the two.

- [X] T004 Delete the orphaned compiled migration artifact in `backend/apps/reservations/migrations/__pycache__/` (the `0004_add_updated_by.cpython-*.pyc` file)

**Checkpoint**: Foundation ready — all user stories can now proceed independently

---

## Phase 3: User Story 1 - Remove redundant reservations list view (Priority: P1) 🎯 MVP

**Goal**: Remove the `/reservations/list/` endpoint and its dead view, template, and tests so the reservations module has a single canonical list view.

**Independent Test**: Navigate to `/reservations/list/` → 404; `/reservations/` still works with all filters.

### Implementation for User Story 1

- [X] T005 [US1] Remove `reservation_list_by_slot` view function from `backend/apps/reservations/views.py`
- [X] T006 [US1] Delete the unused template at `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`
- [X] T007 [US1] Remove the `list/` URL route from `backend/apps/reservations/urls.py`
- [X] T008 [US1] Remove the `list/` URL route reference from `backend/config/urls.py` (if present)
- [X] T009 [US1] Remove test classes that exclusively cover `/reservations/list/` (`TestClientColumnNoEmail`, `TestReservationsList`) from `backend/tests/test_reservations_list.py`

**Checkpoint**: At this point, `/reservations/list/` returns 404 and `/reservations/` works as before.

---

## Phase 4: User Story 2 - Preserve and relocate Export PDF (Priority: P1)

**Goal**: Relocate PDF export from `/reservations/list/pdf/` to `/reservations/pdf/` so users can still export from the main reservations page.

**Independent Test**: Visit PDF export URL with valid parameters and receive a downloadable PDF with correct filename and content type.

### Implementation for User Story 2

- [X] T010 [P] [US2] Update PDF route in `backend/apps/reservations/urls.py` from `list/pdf/` to `pdf/`
- [X] T011 [US2] Update the Export PDF button URL in `backend/apps/reservations/templates/reservations/reservation_list.html` to point to `reservations:reservation-list-pdf`
- [X] T012 [US2] Update any other template references to the old PDF URL (confirm none exist via search)

**Checkpoint**: At this point, `/reservations/pdf/?class_slot=X&date=Y` returns a valid PDF; `/reservations/` page Export PDF button works.

---

## Phase 5: User Story 3 - Complete `updated_by` migration (Priority: P2)

**Goal**: Create a proper Django migration to add `updated_by` field to the Reservation model, completing the abandoned work.

**Independent Test**: Migration runs successfully; Reservation model has an `updated_by` FK field; no orphaned artifacts remain.

### Implementation for User Story 3

- [X] T013 [P] [US3] Add `updated_by` ForeignKey field to Reservation model in `backend/apps/reservations/models.py` (nullable, `SET_NULL`, related_name `updated_reservations`, verbose_name `"Updated by"`)
- [X] T014 [US3] Run `python manage.py makemigrations reservations` to generate the migration file at `backend/apps/reservations/migrations/0004_add_updated_by.py`
- [X] T015 [US3] Run `python manage.py migrate reservations` to apply the new migration
- [X] T016 [US3] Verify the orphaned `.pyc` was deleted in T004 and no longer causes issues

**Checkpoint**: Reservation model includes `updated_by`, migration runs cleanly.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verification and cleanup across all stories

- [X] T017 Run full test suite with `pytest backend/tests/test_reservations_list.py -v` and confirm all retained tests pass
- [X] T018 [P] Run linter with `ruff check backend/apps/reservations/ backend/tests/` to confirm no linting issues
- [X] T019 Run `python manage.py check` to verify Django project integrity
- [X] T020 Run `python manage.py showmigrations reservations` to confirm migration state is clean

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — removes orphaned artifact before migration creation
- **US1 (Phase 3)**: Depends on Setup completion only — independent of US2 and US3
- **US2 (Phase 4)**: Depends on Setup completion only — independent of US1 and US3
- **US3 (Phase 5)**: Depends on Foundational (Phase 2) — orphaned `pyc` must be deleted before `makemigrations`
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories — can be done in any order
- **User Story 2 (P1)**: No dependencies on other stories — can be done in any order
- **User Story 3 (P2)**: Depends on Foundational (orphaned file deletion)

### Within Each User Story

- US1: View → Template → URL → Tests (sequential)
- US2: URL → Template (one after the other)
- US3: Model → Migration → Migrate → Verify (sequential)

### Parallel Opportunities

- All Phase 1 tasks can run in parallel
- US1, US2, and US3 can run in parallel (US3 only after T004)
- T010 and T013 (different files, same phase) can run in parallel
- T018 (linter) can run in parallel with T017 or T019

---

## Parallel Example: User Stories 1, 2, and 3

```bash
# US1: Remove dead endpoint
Task: T005 Remove reservation_list_by_slot view
Task: T006 Delete reservation_list_by_slot.html template
Task: T007 Remove list/ route
Task: T009 Remove dead test classes

# US2: Relocate PDF (can run in parallel with US1)
Task: T010 Update PDF route in urls.py
Task: T011 Update PDF button URL in reservation_list.html

# US3: Migration (after T004)
Task: T013 Add updated_by to model
Task: T014 Generate migration
Task: T015 Apply migration
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (T004 only)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: `/reservations/list/` returns 404; `/reservations/` still works
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Developer completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 + User Story 2
   - Developer B: User Story 3
3. All stories complete, verify with Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Do NOT leave any `0004_add_updated_by.cpython-*.pyc` files behind
