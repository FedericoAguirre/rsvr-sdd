---
description: "Task list for creating reservations list per class slot"
---

# Tasks: Create Reservations List per Class Slot

**Input**: Design documents from `specs/008-reservations-list-per-class/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/reservations/`, `backend/tests/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and review existing codebase

- [X] T001 Create feature branch `008-reservation-lists` from main
- [X] T002 [P] Review existing Reservation model, views, and URL patterns in `backend/apps/reservations/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Install dependencies and configure environment

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Install WeasyPrint system dependencies (`libpango-1.0-0`, `libcairo2`, `libgdk-pixbuf2.0-0`) in Dockerfile at `backend/Dockerfile`
- [X] T004 Add `weasyprint` to project dependencies in `backend/pyproject.toml`
- [X] T005 [P] Review existing test patterns in `backend/tests/test_client_list.py` for conventions (fixtures, auth, assertions)

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 - View Reservations List (Priority: P1) 🎯 MVP

**Goal**: Operator or Administrator can view a reservations list filtered by class slot and date, showing equipment names with client names ordered alphabetically

**Independent Test**: Navigate to `/reservations/list/?class_slot=1&date=2026-06-15` with a logged-in staff user — the page shows the date and class slot name in the header with a table of equipment-client pairs ordered by equipment name

### Tests for User Story 1 (TDD — write first, ensure they FAIL) ⚠️

- [X] T006 [P] [US1] Write test for list page rendering with header (date + class slot name) in `backend/tests/test_reservations_list.py`
- [X] T007 [P] [US1] Write test for equipment-client table ordered alphabetically by equipment name in `backend/tests/test_reservations_list.py`
- [X] T008 [P] [US1] Write test for empty state (no reservations — header shown, empty table) in `backend/tests/test_reservations_list.py`
- [X] T009 [P] [US1] Write test for unauthenticated user being redirected to login in `backend/tests/test_reservations_list.py`

### Implementation for User Story 1

- [X] T010 [US1] Create `reservation_list_by_slot` view in `backend/apps/reservations/views.py` that filters by class_slot and date, orders by equipment__name, and passes query results to template
- [X] T011 [US1] Add URL pattern for the list view at `reservations/list/` in `backend/apps/reservations/urls.py`
- [X] T012 [P] [US1] Create `reservation_list_by_slot.html` template in `backend/apps/reservations/templates/reservations/` with header (date + class slot name), ordered equipment-client table
- [X] T013 [US1] Add i18n labels (`gettext_lazy`) for all UI text in the new template and view
- [X] T014 [US1] Verify tests pass: run `pytest tests/test_reservations_list.py -v`

**Checkpoint**: At this point, User Story 1 should be fully functional — the reservations list page works for any class slot and date combination

---

## Phase 4: User Story 2 - Export Reservations List to PDF (Priority: P2)

**Goal**: Operator or Administrator can download the reservations list as a PDF with the same content as the on-screen view

**Independent Test**: Navigate to `/reservations/list/pdf/?class_slot=1&date=2026-06-15` — a PDF file downloads containing the date, class slot name, and equipment-client table

### Tests for User Story 2 (TDD — write first, ensure they FAIL) ⚠️

- [X] T015 [P] [US2] Write test for PDF download returns correct content type (`application/pdf`) in `backend/tests/test_reservations_list.py`
- [X] T016 [P] [US2] Write test for PDF with empty reservations list (header present, empty table) in `backend/tests/test_reservations_list.py`
- [X] T017 [P] [US2] Write test for PDF export button visible on list page in `backend/tests/test_reservations_list.py`

### Implementation for User Story 2

- [X] T018 [US2] Create `reservation_list_pdf` view in `backend/apps/reservations/views.py` that generates PDF via WeasyPrint from the filtered reservation data
- [X] T019 [US2] Add URL pattern for PDF export at `reservations/list/pdf/` in `backend/apps/reservations/urls.py`
- [X] T020 [P] [US2] Create `reservation_list_pdf.html` template in `backend/apps/reservations/templates/reservations/` styled for print/PDF output with header and equipment-client table
- [X] T021 [US2] Add error handling — if PDF generation fails, show user-friendly error message with retry button (reuse existing message framework)
- [X] T022 [US2] Add i18n labels (`gettext_lazy`) for all text in the PDF template
- [X] T023 [US2] Verify tests pass: run `pytest tests/test_reservations_list.py -v`

**Checkpoint**: Both user stories complete — reservations list viewable on screen and exportable as PDF

---

## Phase 5: User Story 3 - Modify Main Reservations Page with Class Slot Filter (Priority: P2)

**Goal**: The main Reservations page (`/reservations/`) includes a class slot filter alongside the existing date filter, and displays the per-slot equipment-client table when both a class slot and date are selected.

**Independent Test**: Navigate to `/reservations/?class_slot=1&date=2026-06-15` as an Operator — the page shows a class slot dropdown, date filter, "New Reservation" button, and a table of equipment-client pairs ordered by equipment name.

### Tests for User Story 3 (TDD — write first, ensure they FAIL) ⚠️

- [X] T024 [P] [US3] Write test for class slot + date filter showing equipment-client pairs on main page in `backend/tests/test_reservations_list.py`
- [X] T025 [P] [US3] Write test for "New Reservation" button remaining visible when filter active in `backend/tests/test_reservations_list.py`
- [X] T026 [P] [US3] Write test for class slot dropdown present on main page in `backend/tests/test_reservations_list.py`
- [X] T027 [P] [US3] Write test for empty state with appropriate message on main page in `backend/tests/test_reservations_list.py`

### Implementation for User Story 3

- [X] T028 [US3] Modify `reservation_list` view in `backend/apps/reservations/views.py` to accept `class_slot` param and switch to equipment-client ordering when both class_slot and date are selected
- [X] T029 [US3] Add class slot filter dropdown to the `reservation_list.html` template in `backend/apps/reservations/templates/reservations/`
- [X] T030 [US3] Update `reservation_list.html` to display per-slot equipment-client table when class_slot is active
- [X] T031 [US3] Add i18n labels (`gettext_lazy`) for all new UI text in the modified template
- [X] T032 [US3] Verify tests pass: run `pytest tests/test_reservations_list.py -v`

**Checkpoint**: All three user stories complete — per-slot list viewable on `/reservations/list/`, as PDF, and inline on the main `/reservations/` page

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T033 [P] Update Dockerfile in `backend/Dockerfile` with WeasyPrint system dependencies (libpango, libcairo, libgdk-pixbuf)
- [X] T034 [P] Update `.env.example` if any new environment variables were added
- [X] T035 [P] Run full test suite: `pytest tests/ -v` — confirm all tests pass
- [X] T036 [P] Move `ai/features/todos/01_create_reservations_list_per_class.md` to `ai/features/done/`
- [X] T037 Run quickstart.md verification steps to confirm feature works end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3–5)**: All depend on Foundational phase completion
  - US2 depends on US1 (PDF view reuses US1's data query logic)
  - US3 depends on US1 (reuses `_get_slot_reservations` helper)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories — can start immediately after Foundation
- **User Story 2 (P2)**: Depends on US1 (reuses the reservation query and data context)
- **User Story 3 (P2)**: Depends on US1 (reuses `_get_slot_reservations` helper and per-slot template patterns)

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Models/data layer before views
- Views before templates
- Templates before i18n
- Tests verification before story checkpoint

### Parallel Opportunities

- T002 can run in parallel with T001
- T003, T004, T005 can run in parallel
- All test tasks for a story (`[P] [US1]` or `[P] [US2]`) can run in parallel
- T012 and T013 for US1 template + i18n can run in parallel
- T020 and T022 for US2 template + i18n can run in parallel
- All test tasks for US3 (`[P] [US3]`) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Write tests in parallel:
Task: "T006 - List page rendering test"
Task: "T007 - Ordering test"
Task: "T008 - Empty state test"
Task: "T009 - Unauthenticated test"

# Verify all fail:
pytest tests/test_reservations_list.py -v

# Implement view + template in parallel:
Task: "T010 - Create view"
Task: "T012 - Create HTML template"
```

---

## Parallel Example: User Story 2

```bash
# Write tests in parallel:
Task: "T015 - PDF content type test"
Task: "T016 - PDF empty state test"
Task: "T017 - Export button test"

# All fail initially, then implement:
Task: "T018 - Create PDF view"
Task: "T020 - Create PDF template"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (WeasyPrint install)
3. Complete Phase 3: User Story 1 (Reservations list page)
4. **STOP and VALIDATE**: Navigate to `/reservations/list/?class_slot=1&date=2026-06-15` — list displays correctly
5. Deploy/demo if ready (on-screen list is the MVP)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---

## Notes

- All new UI text MUST use Django i18n (`gettext_lazy`/`gettext`) with Spanish translations in `backend/locale/es/`
- WeasyPrint requires system libraries — update Dockerfile in Phase 5 (or Phase 2 if Docker is used for dev)
- The existing `Reservation` model has no status field — the "active only" filter is a no-op in v1
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
