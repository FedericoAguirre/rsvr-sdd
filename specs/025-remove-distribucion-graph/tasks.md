---

description: "Task list for removing the Distribution graph from the payments reports page"

---

# Tasks: Remove Distribution Graph

**Input**: Design documents from `/specs/025-remove-distribucion-graph/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No test tasks — TDD exemption granted in plan (pure deletion with no new logic).

**Organization**: Single user story (P1). No setup or foundational phases needed — this is a straightforward template edit.

## Format: `[ID] [P] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **File to modify**: `backend/apps/payments/templates/payments/payment_reports.html`

---

## Phase 1: User Story 1 - Admin views cleaner payment reports page (Priority: P1) 🎯 MVP

**Goal**: Remove the redundant Distribution pie chart from the payments/reports/ page and widen the remaining Totals bar chart to full width.

**Independent Test**: Navigate to `/payments/reports/` and confirm only one chart (the bar chart) is visible. Check browser console for zero JS errors. The layout should fill the full column width with no empty card frames.

### Implementation for User Story 1

- [x] T001 [US1] Widen Totals column by changing `col-md-6` to `col-12` on the outer div at line 38 in `backend/apps/payments/templates/payments/payment_reports.html`
- [x] T002 [P] [US1] Remove the Distribution card column (lines 48-57) containing the `distributionChart` canvas and its wrapper div in `backend/apps/payments/templates/payments/payment_reports.html`
- [x] T003 [P] [US1] Remove the pie chart JavaScript block (lines 107-122) that instantiates the `distributionChart` in `backend/apps/payments/templates/payments/payment_reports.html`
- [x] T004 [US1] Verify the page renders correctly — load `/payments/reports/`, confirm only one chart appears, check browser console for JS errors, and verify existing payment tests still pass with `python -m pytest backend/tests/test_payments.py`

**Checkpoint**: User Story 1 complete — the reports page displays a single full-width bar chart with no errors.

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (P1)**: No dependencies — can start immediately. T002 and T003 are independent of each other ([P]) and can run in parallel. T001 must be completed before or alongside T002 (they modify adjacent lines). T004 is the verification step and must run last.

### Parallel Opportunities

- T002 and T003 can run in parallel (different sections of the same file — unlikely to conflict if edited carefully)
- T001 and T002 modify adjacent lines; preferably done sequentially or together

---

## Parallel Example: User Story 1

```bash
# T002 and T003 can be done in parallel:
Task: "Remove the Distribution card column (lines 48-57) from backend/apps/payments/templates/payments/payment_reports.html"
Task: "Remove the distribution chart JS (lines 107-122) from backend/apps/payments/templates/payments/payment_reports.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001: Widen the Totals column
2. Complete T002: Remove the Distribution card
3. Complete T003: Remove the pie chart JS
4. Complete T004: Verify everything works
5. **STOP and VALIDATE**: Test by loading the reports page
6. Deliver/demo — the feature is complete

---

## Notes

- [P] tasks = different sections of the same file, safe to edit independently
- [US1] label maps task to User Story 1
- The single user story is independently completable and testable
- Commit after each task or logical group
- Verify browser console shows no JS errors after removal
