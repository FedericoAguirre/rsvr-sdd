# Tasks: Consistent Reservations List

**Input**: Design documents from `specs/015-consistent-reservations-list/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included per Constitution mandate (TDD required).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Django web app**: `backend/apps/...`, `backend/tests/...`

---

## Phase 1: Setup

**Purpose**: Review design docs and verify environment

- [x] T001 Review design documents in `specs/015-consistent-reservations-list/` (plan.md, research.md, spec.md)
- [x] T002 Verify on branch `016-consistent-reservations-list` with `git branch`

---

## Phase 2: User Story 1 - View reservations with consistent fields (Priority: P1) 🎯 MVP

**Goal**: The reservations list always displays the same six fields (Date, Client, Class Slot, Equipment, Status, View) regardless of filter state.

**Independent Test**: Navigate to `/reservations/`, apply a filter via the form, and verify all six field headers are still present in the HTML table.

### Tests for User Story 1 ⚠️ TDD — Write FIRST, ensure they FAIL before implementation

- [x] T003 [P] [US1] Write test verifying all six column headers appear on initial page load at `GET /reservations/` in `backend/tests/test_reservations_list.py`
- [x] T004 [P] [US1] Write test verifying all six column headers appear after applying a class_slot+date filter at `GET /reservations/?class_slot=X&date=Y` in `backend/tests/test_reservations_list.py`
- [x] T005 [P] [US1] Write test verifying all six column headers appear after clearing a filter (navigating from filtered URL to `GET /reservations/`) in `backend/tests/test_reservations_list.py`

### Implementation for User Story 1

- [x] T006 [US1] Fix `backend/apps/reservations/templates/reservations/reservation_list.html` — remove `{% if class_slot %}` branching around the table, always render the full 6-column table (Date, Client, Class Slot, Equipment, Status, View)
- [x] T007 [P] [US1] Fix `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html` — add Date, Class Slot, and View columns to match the full 6-column format
- [x] T008 [US1] Verify tests from T003-T005 now pass: run `cd backend && python -m pytest tests/test_reservations_list.py -v`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently — the reservations list shows all six fields in every view state.

---

## Phase 3: User Story 2 - Export PDF remains unaffected (Priority: P2)

**Goal**: The Export PDF functionality produces the same output as before the change — zero regressions.

**Independent Test**: Export a reservation as PDF from the filtered list view and verify the output matches the expected format.

### Tests for User Story 2 ⚠️ TDD — Write FIRST, ensure they FAIL before implementation

- [x] T009 [P] [US2] Write regression test for PDF export content type and filename format at `GET /reservations/list/pdf/?class_slot=X&date=Y` in `backend/tests/test_reservations_list.py`
- [x] T010 [P] [US2] Write regression test verifying PDF export with status filter at `GET /reservations/list/pdf/?class_slot=X&date=Y&status=used` in `backend/tests/test_reservations_list.py`

### Implementation for User Story 2

- [x] T011 [US2] Verify no changes were made to PDF template (`reservation_list_pdf.html`) or PDF view — run all existing PDF tests: `cd backend && python -m pytest tests/test_reservations_list.py::TestReservationsListPDF -v`

**Checkpoint**: All PDF tests pass, confirming zero regressions from the template changes.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation updates

- [x] T012 [P] Run full test suite: `cd backend && python -m pytest -v`
- [x] T013 Update `AGENTS.md` to confirm plan reference at `specs/015-consistent-reservations-list/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion — BLOCKS all other stories
- **User Story 2 (Phase 3)**: Depends on User Story 1 implementation (template changes could affect PDF path)
- **Polish (Phase 4)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: MVP — the core fix. All tests can be written and run independently.
- **User Story 2 (P2)**: Regression verification — confirms no side effects from US1 changes.

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Constitution mandates TDD)
- Implementation then makes tests pass
- The changes are template-only; no models, services, or endpoints to create

### Parallel Opportunities

- T003, T004, T005 (test writing for US1) can run in parallel
- T006 and T007 (template fixes) can run in parallel (different files)
- T009 and T010 (test writing for US2) can run in parallel
- T012 and T013 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test for initial page load column headers"
Task: "Write test for filtered view column headers"
Task: "Write test for cleared filter column headers"

# Launch both template fixes together:
Task: "Fix reservation_list.html"
Task: "Fix reservation_list_by_slot.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (review docs, verify branch)
2. Complete Phase 2: User Story 1 (tests → template fix → tests pass)
3. **STOP and VALIDATE**: Verify all six columns in all view states
4. Deploy/demo if ready

### Incremental Delivery

1. Phase 1 → Ready to work
2. Phase 2 (US1) → Test independently → Deploy/demo (MVP!)
3. Phase 3 (US2) → Verify no regressions → Deploy
4. Phase 4 (Polish) → Final suite pass

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Do NOT modify `reservation_list_pdf.html` or PDF-related views (out of scope per FR-004)
