# Tasks: Quick Reservation Status Management

**Input**: Design documents from `/specs/019-quick-reservation-status/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Test tasks are included per TDD requirements in the project constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/`, `backend/tests/` at repository root
- All template files under `backend/apps/reservations/templates/reservations/`
- All test files under `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

None required — the project is already set up with Django, HTMX 2.0, Bootstrap 5.3. No new dependencies needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared infrastructure required by ALL user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 [P] Create `reservation_extras.py` template tag with `status_badge_class` filter in `backend/apps/reservations/templatetags/reservation_extras.py`
- [x] T002 [P] Create `reservation_row.html` partial template for HTMX row swap in `backend/apps/reservations/templates/reservations/partials/reservation_row.html`

**Checkpoint**: Foundation ready — template tag and partial exist and can be loaded

---

## Phase 3: User Story 3 - View reservation status badges at a glance (Priority: P2)

**Goal**: Each reservation row in the list displays a colored badge (green=reserved, blue=used, gray=unused) so operators can identify status at a glance.

**Independent Test**: Load the reservation list with reservations in all three statuses and verify each row shows the correct badge color without any page reload.

### Tests for User Story 3 (TDD) ⚠️

- [x] T003 [P] [US3] Write test verifying status badge class mapping in `backend/tests/test_reservations_list.py`
- [x] T004 [P] [US3] Write test verifying badge rendering in list view per status in `backend/tests/test_reservations_list.py`

### Implementation for User Story 3

- [x] T005 [P] [US3] Add status badge rendering to `reservation_list.html` in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [x] T006 [P] [US3] Add status badge rendering to `reservation_list_by_slot.html` in `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`

**Checkpoint**: All reservation rows show colored status badges. Operators can identify status at a glance.

---

## Phase 4: User Stories 1 & 2 - Mark reservation as used/unused from list view (Priority: P1) 🎯 MVP

**Goal**: Operators can click inline "Mark as used" or "Mark as unused" buttons on any reservation row to change its status without navigating to the detail page. Status updates instantly via HTMX without page reload.

**Independent Test**: Load the reservation list, click "Mark as used" on a reserved reservation — verify badge changes to blue and text reads "Used". Click "Mark as unused" — verify badge changes to gray. Both should happen without page reload.

### Tests for User Stories 1 & 2 (TDD) ⚠️

- [x] T007 [P] [US1/US2] Write test for HTMX request returning row partial (status 200, HTML contains `<tr`) in `backend/tests/test_reservations_list.py`
- [x] T008 [P] [US1/US2] Write test for non-HTMX request still redirecting to detail page in `backend/tests/test_reservations_list.py`
- [x] T009 [P] [US1/US2] Write test for invalid status via HTMX returning 400 in `backend/tests/test_reservations_list.py`
- [x] T010 [P] [US1/US2] Write test for unauthenticated HTMX request redirecting to login in `backend/tests/test_reservations_list.py`
- [x] T011 [P] [US1/US2] Write test for marking reserved→used updates badge and status in `backend/tests/test_reservations_list.py`
- [x] T012 [P] [US1/US2] Write test for marking used→unused updates badge and status in `backend/tests/test_reservations_list.py`

### Implementation for User Stories 1 & 2

- [x] T013 [US1/US2] Modify `reservation_change_status` view in `backend/apps/reservations/views.py` to return HTMX partial response with HX-Trigger header
- [x] T014 [P] [US1/US2] Add inline "Mark as used" / "Mark as unused" action buttons to `reservation_list.html` in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [x] T015 [P] [US1/US2] Add inline "Mark as used" / "Mark as unused" action buttons to `reservation_list_by_slot.html` in `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`

**Checkpoint**: Both inline actions work on both list views. Status changes are instant via HTMX. All tests pass.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and project housekeeping

- [x] T016 [P] Run Ruff linter and fix any issues
- [x] T017 [P] Verify all user-facing strings use i18n translation calls
- [x] T018 [P] Run full test suite to verify nothing is broken
- [x] T019 Move `ai/features/todos/02a_quick_reservation_status_management.md` to `ai/features/done/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — can start immediately
- **US3 — Badges (Phase 3)**: Depends on Foundational (Phase 2) — requires template tag and partial
- **US1/US2 — Mark used/unused (Phase 4)**: Depends on Foundational (Phase 2) — requires the partial template for HTMX response
- **Polish (Phase 5)**: Depends on all desired phases being complete

### User Story Dependencies

- **US3 (P2)**: Can start after Foundational — No dependencies on other stories
- **US1/US2 (P1)**: Can start after Foundational — templates co-exist with US3 badges but are independently testable

### Within Each Phase

- Tests (TDD) MUST be written and FAIL before implementation
- Templates before view changes (for HTML reference)
- Core implementation before integration

### Parallel Opportunities

- T001 and T002 (template tag + partial) can run in parallel
- T003 and T004 (US3 tests) can run in parallel
- T005 and T006 (US3 implementation) can run in parallel
- T007–T012 (US1/US2 tests) can all run in parallel
- T014 and T015 (action buttons in both templates) can run in parallel
- T016–T019 (Polish) can mostly run in parallel

---

## Parallel Example: User Story 3

```bash
# Launch both template changes together:
Task: "Add status badge to reservation_list.html"
Task: "Add status badge to reservation_list_by_slot.html"
```

## Parallel Example: User Stories 1 & 2

```bash
# Launch all tests together:
Task: "Write HTMX row partial test"
Task: "Write non-HTMX redirect test"
Task: "Write invalid status test"
Task: "Write unauthenticated test"
Task: "Write reserved-to-used test"
Task: "Write used-to-unused test"

# Launch both template changes together:
Task: "Add inline buttons to reservation_list.html"
Task: "Add inline buttons to reservation_list_by_slot.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 2: Foundational (template tag + partial)
2. Complete Phase 4: User Stories 1 & 2 (the core P1 feature)
3. **STOP and VALIDATE**: Test marking reservations used/unused from list
4. Deploy/demo if ready
5. Add Phase 3: US3 badges (they complete the UX but the MVP works without them in terms of functionality)

### Incremental Delivery

1. Complete Foundational → Foundation ready
2. Add US1/US2 (mark used/unused) → Test independently → Deploy/Demo (MVP!)
3. Add US3 (badges) → Test independently → Deploy/Demo (polish)

### Single Developer Strategy

1. Phase 2 (template tag + partial)
2. Phase 3 (badges - quick wins, builds visual foundation)
3. Phase 4 (inline actions - the meat of the feature)
4. Phase 5 (polish)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests MUST fail before implementing (TDD per constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- This feature modifies existing code — no new migrations or models needed
