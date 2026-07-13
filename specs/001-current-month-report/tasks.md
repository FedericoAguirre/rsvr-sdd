# Tasks: Current Month Payments Report

**Input**: Design documents from `specs/001-current-month-report/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests included per TDD requirement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root — adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

No setup tasks required — the project is fully initialized with all dependencies installed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

No foundational tasks required — the existing Django app, database, and testing infrastructure are already in place.

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — Current Month Auto-Preselection (Priority: P1) 🎯 MVP

**Goal**: When the user navigates to the payments reports page with no query params, the start/end date fields are pre-filled with the first/last day of the current month.

**Independent Test**: Load `/payments/reports/` (no query params) and verify that `start_date` and `end_date` in the response context equal the first and last day of the current month.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [P] [US1] Test: default dates match current month boundaries in `backend/tests/test_payments.py`
- [x] T002 [P] [US1] Test: explicit query params override defaults in `backend/tests/test_payments.py`
- [x] T003 [US1] Test: empty dates fall back to current month in `backend/tests/test_payments.py`

### Implementation for User Story 1

- [x] T004 [US1] Add current-month default logic in `PaymentReportView.get_context_data()` in `backend/apps/payments/views.py` — set `start` to first day of current month and `end` to last day when params are empty

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Auto-Render with Current Month Data (Priority: P1)

**Goal**: Once the page loads with current month defaults, the earnings report and graph render without extra user action.

**Independent Test**: Load `/payments/reports/` (no query params) and verify that `report_data` context contains aggregated payments for current month and template renders the chart.

### Tests for User Story 2 ⚠️

- [x] T005 [P] [US2] Test: report data is present in initial page context for current month in `backend/tests/test_payments.py`
- [x] T006 [US2] Test: current month with no payments returns empty state response in `backend/tests/test_payments.py`

### Implementation for User Story 2

- [x] T007 [US2] Verify auto-render — since US1 defaults the dates and the existing template renders from context, confirm the chart renders on DOM ready (no JS changes needed) in `backend/apps/payments/templates/payments/payment_reports.html`

**Checkpoint**: At this point, User Story 2 should be fully functional — the page auto-renders on load

---

## Phase 5: User Story 3 — Manual Date Override (Priority: P2)

**Goal**: After initial load with defaults, user can modify date fields and re-query for a different period. On navigation away and back, dates reset to current month.

**Independent Test**: Submit the report form with explicit start/end dates and verify the report updates; then navigate away and back, confirm dates reset to current month.

### Tests for User Story 3 ⚠️

- [x] T008 [P] [US3] Test: non-current-month dates via query params override defaults in `backend/tests/test_payments.py`
- [x] T009 [US3] Test: navigating to page without query params resets to current month in `backend/tests/test_payments.py`

### Implementation for User Story 3

- [x] T010 [US3] Verify manual override — existing form submission already passes `start`/`end` params and the view respects them; confirm no regression in `backend/apps/payments/views.py`
- [x] T011 [US3] Verify reset behavior — since defaults are only applied when params are empty, navigating with no params returns current month; confirm existing browser navigation behavior

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T012 Run all tests pass: `docker compose exec web uv run pytest tests/test_payments.py -v`
- [x] T013 Verify existing export functionality at `/payments/reports/export/` still works with defaulted dates
- [x] T014 Verify existing manual date queries still work (no regression)
- [x] T015 Save AI session file in `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — already complete
- **Foundational (Phase 2)**: No dependencies — already complete
- **User Stories (Phase 3+)**: All depend on existing infrastructure
  - **US1 (Phase 3)**: Must be completed first (provides default dates that US2 relies on)
  - **US2 (Phase 4)**: Depends on US1 — auto-render is a consequence of defaulting dates
  - **US3 (Phase 5)**: Independent of US1/US2 — manual override already works
- **Polish (Phase 6)**: Depends on all stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — can start immediately
- **User Story 2 (P1)**: Depends on US1 completion (auto-render requires default dates)
- **User Story 3 (P2)**: No dependencies on other stories — fully independent

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation then makes tests pass
- Story complete before moving to next priority

### Parallel Opportunities

- T001, T002 (US1 tests) can run in parallel
- T005 (US2 test) can start after T001 completes
- T008 (US3 test) is independent — can run in parallel with US1/US2 tasks

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "T001 Test default dates match current month"
Task: "T002 Test explicit params override defaults"

# Launch implementation after tests fail:
Task: "T004 Add current-month default logic in PaymentReportView.get_context_data()"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 — date defaults
2. **STOP and VALIDATE**: Test US1 independently
3. Deploy/demo if ready — US2 auto-render comes for free

### Incremental Delivery

1. Add User Story 1 → Auto-prefill works! (MVP)
2. Add User Story 2 → Auto-render works (comes with US1)
3. Add User Story 3 → Manual override works (already works, just test)
4. Each story adds value without breaking previous stories

### Environment Reference

When writing script fragments, task execution steps, or running the code, always use these exact commands:
- **Run tests**: `docker compose exec web uv run pytest`
- **Run specific test**: `docker compose exec web uv run pytest tests/test_payments.py -v -k <test_name>`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No new dependencies, no schema changes — purely view logic
