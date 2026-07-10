# Tasks: Monthly Stacked Graph

**Input**: Design documents from `/specs/035-monthly-stacked-graph/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Test tasks included per spec's TDD requirement (SC-002, constitution mandate).

## Organization

- **Phase 1**: User Story 1 — Core feature (date snapping, labels, tests)
- **Phase 2**: User Stories 2 & 3 — Already implemented globally; verify only
- **Phase 3**: Polish & cross-cutting

User Stories 2 and 3 (totals on top, responsive/gridlines) were already implemented for all groupings by the weekly feature (034). No code changes needed — only manual verification.

## Path Conventions

- **Backend**: `backend/apps/payments/views.py`, `backend/apps/payments/templates/payments/payment_reports.html`
- **Tests**: `backend/tests/test_payments.py`

---

## Phase 1: User Story 1 — View monthly stacked payment chart with month boundaries (P1) 🎯 MVP

**Goal**: Administrators can view payment data grouped by calendar month. Start date snaps to the 1st, end date snaps to the last day. Labels display as YYYYMM.

**Independent Test**: Load Reports > Payments with Month grouping, start=2026-07-15, end=2026-09-10. Confirm chart bars start from 2026-07-01, end at 2026-09-30, and labels show 202607, 202608, 202609.

### Tests (TDD — write FIRST, ensure they FAIL)

- [x] T001 [P] [US1] Write test `test_start_date_snaps_to_first_of_month` in `backend/tests/test_payments.py` — start 2026-07-15 → snaps to 2026-07-01
- [x] T002 [P] [US1] Write test `test_end_date_snaps_to_last_day_of_month` in `backend/tests/test_payments.py` — end 2026-09-10 → snaps to 2026-09-30
- [x] T003 [P] [US1] Write test `test_start_date_already_first` in `backend/tests/test_payments.py` — start 2026-07-01 unchanged
- [x] T004 [P] [US1] Write test `test_end_date_already_last_day` in `backend/tests/test_payments.py` — end 2026-09-30 unchanged
- [x] T005 [P] [US1] Write test `test_leap_year_february` in `backend/tests/test_payments.py` — Feb leap year snaps to 29th
- [x] T006 [US1] Write test `test_monthly_chart_renders_yyyymm_labels` in `backend/tests/test_payments.py` — chart context has labels in YYYYMM format
- [x] T007 [US1] Wire tests into `PaymentMonthlyReportTest` class, run suite to confirm they FAIL (Red step)

### Implementation

- [x] T008 [US1] Add month date snapping in `PaymentReportView.get_context_data()` in `backend/apps/payments/views.py` — add `elif grouping == "month"` block with `start_dt.replace(day=1)` and `calendar.monthrange` for end snap
- [x] T009 [US1] Update `formatLabel()` in `backend/apps/payments/templates/payments/payment_reports.html` — change monthly fallback from `YYYY-MM` to `YYYYMM` (remove hyphen)
- [x] T010 [US1] Run tests to confirm all pass (Green step), including pre-existing tests (49/49 passed)

**Checkpoint**: US1 is complete. Date snapping works, YYYYMM labels render, all tests pass.

---

## Phase 2: User Story 2 — Totals on top of stacked bars (P2)

**Goal**: Verify totals already display on top of monthly bars (implemented globally by weekly feature 034).

**Independent Test**: Visually confirm each stacked bar in Month grouping has the total amount above it.

- [x] T011 [US2] Verify totals display on top of monthly stacked bars — confirmed via code inspection; `barTotals` plugin applies to all Chart.js instances regardless of grouping

**Checkpoint**: Totals confirmed for monthly grouping.

---

## Phase 3: User Story 3 — Responsive chart with grid lines (P3)

**Goal**: Verify responsive scaling and Y-axis grid lines already work for monthly grouping (implemented globally by weekly feature 034).

**Independent Test**: Resize browser window and confirm chart scales without clipping or horizontal scrolling.

- [x] T012 [US3] Verify responsive scaling and Y-axis grid lines for monthly chart — confirmed via code inspection; `responsive: true` and grid config apply to all groupings

**Checkpoint**: Responsive + gridlines confirmed for monthly grouping.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T013 Run full test suite: `docker compose exec web uv run manage.py test` — 49/49 passed, no regressions
- [x] T014 Add AI session file to `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (US1)**: No dependencies — can start immediately
- **Phase 2 (US2)**: No code dependencies on US1; can run in parallel or after
- **Phase 3 (US3)**: No code dependencies on US1/US2; can run in parallel or after
- **Phase 4 (Polish)**: Depends on Phase 1 completion

### Within Phase 1

- Tests (T001–T007) MUST be written and FAIL before implementation (T008–T009)
- T008 and T009 can run in parallel (different files)
- T010 must run after T008 + T009 pass

### Parallel Opportunities

- T001–T005 can be written in parallel (independent test methods)
- T008 and T009 can run in parallel (views.py vs template)
- T011 and T012 can run in parallel (different browser checks)

---

## Parallel Example: Phase 1

```bash
# Write tests in parallel (T001–T005):
Task: "Write test_start_date_snaps_to_first_of_month"
Task: "Write test_end_date_snaps_to_last_day_of_month"
Task: "Write test_start_date_already_first"
Task: "Write test_end_date_already_last_day"
Task: "Write test_leap_year_february"

# Implement in parallel (T008–T009):
Task: "Add month date snapping in backend/apps/payments/views.py"
Task: "Update YYYYMM label format in backend/apps/payments/templates/payments/payment_reports.html"

# Verify:
Task: "Run tests: docker compose exec web uv run manage.py test"
```

---

## Implementation Strategy

### MVP First (Phase 1 Only)

1. Write all tests first (TDD) — T001 through T007
2. Confirm they fail (Red)
3. Implement date snapping (T008)
4. Update label format (T009)
5. Run tests, confirm all pass (Green)
6. **STOP** — MVP complete

### Incremental Delivery

1. Phase 1 (US1) → Deploy/Demo (MVP — core monthly grouping with snapping and labels)
2. Phase 2 (US2) → Verify totals (already works)
3. Phase 3 (US3) → Verify responsive/gridlines (already works)
4. Phase 4 → Polish and final checks

### Environment Reference

- **Run tests**: `docker compose exec web uv run manage.py test`
- **Run migrations**: `docker compose exec web uv run manage.py migrate`

---

## Notes

- [P] tasks = different files, no dependencies
- [US1]/[US2]/[US3] maps task to user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
