# Tasks: Stacked Graph Weekly Grouping

**Input**: Design documents from `/specs/034-stacked-graph-weekly-grouping/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/payments/views.py`, `backend/apps/payments/templates/payments/payment_reports.html`, `backend/tests/test_payments.py`
- Paths adjusted for Django monolith structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No new project infrastructure needed — existing Chart.js v4, Django, and PostgreSQL stack are sufficient. The existing daily chart infrastructure is already deployed.

No tasks.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites. The existing `PaymentReportView` already has a `grouping == "week"` branch with `date_trunc('week', date)`. Date snapping and chart configuration build on existing code.

No tasks.

**Checkpoint**: Ready for user story implementation.

---

## Phase 3: User Story 1 — View weekly stacked payment chart with ISO week boundaries (Priority: P1) 🎯 MVP

**Goal**: An administrator can select "Week" grouping on Reports > Payments and see a stacked bar chart where each bar represents an ISO week (Monday–Sunday). Start date snaps to the closest preceding Monday, end date snaps to the closest following Sunday. Bars are labeled with Monday dates in YYYYMMDD format. Empty weeks are omitted.

**Independent Test**: Load Reports > Payments with Week grouping and dates e.g. start=2026-07-03 (Friday) and end=2026-07-19 (Sunday). Confirm the chart shows bars starting from Monday 2026-07-06 and ending at Sunday 2026-07-19, labeled with Monday dates.

### Tests for User Story 1

- [X] T001 [P] [US1] Write date snapping tests in `backend/tests/test_payments.py`: test that a Friday start snaps to the previous Monday, a Sunday end snaps to the same Sunday, a Monday start stays as-is, and a Tuesday end snaps to the following Sunday
- [X] T002 [P] [US1] Write weekly chart rendering test in `backend/tests/test_payments.py`: test that `grouping=week` returns data with `week` keys in YYYYMMDD format and `payment_type` breakdown
- [X] T003 [US1] Write empty-state test in `backend/tests/test_payments.py`: test that a date range with no payments in Week grouping shows the empty state message

### Implementation for User Story 1

- [X] T004 [P] [US1] Add date snapping logic to `PaymentReportView.get_context_data()` in `backend/apps/payments/views.py`: snap `start` to closest preceding Monday and `end` to closest following Sunday using `date.weekday()` arithmetic when `grouping == "week"`
- [X] T005 [P] [US1] Update `context["start_date"]` and `context["end_date"]` in `PaymentReportView.get_context_data()` in `backend/apps/payments/views.py` so the date input fields display snapped values
- [X] T006 [US1] Add `grouping === "week"` branch in the chart JS block in `backend/apps/payments/templates/payments/payment_reports.html`: configure x-axis with YYYYMMDD Monday-date labels, reuse existing stacked bar dataset construction and tooltip formatting from the daily config
- [X] T007 [US1] Add i18n key for "Failed to load chart data." error message in `backend/locale/es/LC_MESSAGES/django.po` and recompile `.mo` via `docker compose exec web uv run manage.py compilemessages`

**Checkpoint**: At this point, User Story 1 should be fully functional — the chart shows weekly stacked bars with correct ISO week boundaries, date snapping, and proper error handling.

---

## Phase 4: User Story 2 — Stacked columns show totals on top (Priority: P2)

**Goal**: Each weekly stacked bar displays the total payment amount on top for quick visual reference.

**Independent Test**: Visually confirm that each stacked bar in Week grouping has the total amount displayed above it.

### Implementation for User Story 2

- [X] T008 [US2] Add a custom `afterDraw` plugin (`barTotals`) in `backend/apps/payments/templates/payments/payment_reports.html` that renders total amounts above each stacked bar; applies to all groupings including week

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently — weekly bars have totals on top.

---

## Phase 5: User Story 3 — Chart is responsive with grid lines (Priority: P3)

**Goal**: The weekly chart scales proportionally on different viewport sizes without horizontal scrolling, and Y-axis displays horizontal divisory lines.

**Independent Test**: Resize the browser window and confirm the chart resizes proportionally without clipping or horizontal scrolling.

### Implementation for User Story 3

- [X] T009 [US3] Verify the responsive config (`responsive: true`) and Y-axis grid line config from the existing daily chart are applied to all groupings in `backend/apps/payments/templates/payments/payment_reports.html`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Testing, linting, and final verification.

- [X] T010 Run test suite — 41/41 passed (7 new weekly tests, 34 existing)
- [ ] T011 Skip — ruff not installed in container (no lint infrastructure)
- [X] T012 Move `ai/features/todos/06-1-stacked-graph-weekly-grouping.md` to `ai/features/done/06-1-stacked-graph-weekly-grouping.md`
- [ ] T013 Save AI session summary to `ai/sessions/deepseek-v4-flash-free-034-stacked-graph-weekly-grouping-20260710T<timestamp>.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No tasks — can start immediately
- **Foundational (Phase 2)**: No tasks — can start immediately
- **User Stories (Phase 3+)**: All affect `payment_reports.html` (US1) or verify it (US2, US3), so MUST be sequential:
  - US1 (Phase 3) must be complete before US2 (Phase 4) and US3 (Phase 5)
  - US2 (Phase 4) must be complete before US3 (Phase 5)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — start here
- **User Story 2 (P2)**: Depends on US1 — totals config needs weekly chart to exist
- **User Story 3 (P3)**: Depends on US1 — responsive config needs weekly chart to exist

### Within Each User Story

- Tests (T001–T003) MUST be written, committed, and verified FAILING before implementation (TDD)
- Backend tasks (T004–T005) before frontend (T006) — view returns data before chart renders it

### Parallel Opportunities

- T001, T002, T003 (different test methods in same file) — can be written in parallel
- T004 and T005 (both in views.py) — can be written together as they modify the same method
- T004/T005 (views.py) and T006 (template) can run in parallel — different files, no dependency
- T007 (i18n django.po) can run in parallel with T004–T006 entirely — different file, no dependency
- T010 (test run) depends on all code being written first

---

## Parallel Example: User Story 1

```bash
# T001, T002, T003 can be written together (all in test_payments.py):
Task: "Write date snapping tests in test_payments.py"
Task: "Write weekly chart rendering test in test_payments.py"
Task: "Write empty-state test in test_payments.py"

# T004+T005 (views.py) and T007 (django.po) can run in parallel with T006 (template):
Task: "Add date snapping and context updates in views.py"
Task: "Add i18n key in django.po"
Task: "Add weekly chart JS branch in payment_reports.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete tests for US1 (T001–T003) — ensure they fail first (TDD)
2. Complete Phase 3: User Story 1 (date snapping + weekly chart + i18n)
3. **STOP and VALIDATE**: Load Reports > Payments with Week grouping and confirm stacked bars render with correct ISO week boundaries
4. Proceed to US2 and US3 only if time permits

### Incremental Delivery

1. Add User Story 1 → Test independently → Validated (MVP!)
2. Add User Story 2 → Verify datalabels → Validated
3. Add User Story 3 → Verify responsive + gridlines → Validated
4. Each story enhances the chart without breaking previous functionality

### Environment Reference

When running commands, use these exact patterns:
- **Run tests**: `docker compose exec web uv run manage.py test`
- **Recompile .mo**: `docker compose exec web uv run manage.py compilemessages`
- **Run lint**: `docker compose exec web uv run ruff check`
- **Recompile translations**: `docker compose exec web uv run django-admin compilemessages`

---

## Notes

- US1 modifies `views.py` (backend) and `payment_reports.html` (frontend) — both needed for the core feature
- US2 and US3 are verification-only tasks: the datalabels and responsive configs already exist in the daily chart and only need to be carried to the weekly branch
- No new JavaScript libraries allowed — reuse Chart.js v4 already loaded via CDN
- i18n required by constitution for "Failed to load chart data." error message
- All existing report tests must still pass after changes
