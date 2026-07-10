# Tasks: Stacked Graph Daily Grouping

**Input**: Design documents from `/specs/032-stacked-graph-daily-grouping/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/payments/templates/payments/`, `backend/tests/`
- Paths adjusted for Django monolith structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No new project infrastructure needed — existing Chart.js v4, Django, and PostgreSQL stack are sufficient.

No tasks. The feature is a single-file frontend change to `payment_reports.html`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites. The backend (`PaymentReportView`) already returns time-grouped data with `payment_type` breakdown. Only the frontend JS rendering needs to change.

No tasks.

**Checkpoint**: Ready for user story implementation.

---

## Phase 3: User Story 1 — View daily stacked payment chart (Priority: P1) 🎯 MVP

**Goal**: Replace the existing flat bar chart on the Reports > Payments page with a stacked bar chart showing time-grouped payment totals broken down by payment type.

**Independent Test**: Load Reports > Payments with "Day" grouping and visually confirm the chart renders as a stacked bar chart with one bar per day, colored segments per payment type, and an empty state when no data exists.

### Implementation for User Story 1

- [X] T001 [US1] Rewrite chart JS in `backend/apps/payments/templates/payments/payment_reports.html` to transform backend data into time-indexed datasets (one dataset per payment type) instead of the current flat aggregation
- [X] T002 [US1] Configure Chart.js with `scales.x.stacked: true` and `scales.y.stacked: true` in `backend/apps/payments/templates/payments/payment_reports.html`
- [X] T003 [US1] Add empty state handling: show translated message when no payment data exists for selected period in `backend/apps/payments/templates/payments/payment_reports.html`
- [X] T004 [US1] Add i18n translation key for empty state message in `backend/locale/es/LC_MESSAGES/django.po` and recompile `.mo`
- [X] T005 [US1] Verify all four groupings (day, week, month, custom range) render as stacked bars in `backend/apps/payments/templates/payments/payment_reports.html`

**Checkpoint**: At this point, User Story 1 should be fully functional — the chart shows time-grouped stacked bars with proper empty state handling.

---

## Phase 4: User Story 2 — Hover to see payment type breakdown (Priority: P2)

**Goal**: Add tooltips on hover showing the period label, payment type name, and exact total amount for each segment.

**Independent Test**: Hover over any chart segment and verify the tooltip displays the correct date/week label, payment type, and amount.

### Implementation for User Story 2

- [X] T006 [P] [US2] Configure Chart.js tooltip callbacks in `backend/apps/payments/templates/payments/payment_reports.html` to show period label, payment type name, and formatted total amount
- [X] T007 [US2] Verify tooltips display correct data for all groupings (day, week, month, custom range) in `backend/apps/payments/templates/payments/payment_reports.html`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 — Toggle payment types on/off (Priority: P3)

**Goal**: Enable legend interaction so users can click payment type labels to show/hide corresponding segments.

**Independent Test**: Click each legend item and verify the corresponding segments disappear and reappear from the stacked bars.

### Implementation for User Story 3

- [X] T008 [US3] Enable Chart.js legend display with default click-to-toggle behavior in `backend/apps/payments/templates/payments/payment_reports.html` (remove `legend: { display: false }`)
- [X] T009 [US3] Verify all legend items toggle their corresponding segments on/off consistently in `backend/apps/payments/templates/payments/payment_reports.html`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Testing, linting, and final verification.

- [X] T010 Update existing report tests in `backend/tests/test_payments.py` — verified all 12 report tests pass
- [X] T011 Ruff not installed in project — skipped lint (no lint infrastructure)
- [X] T021 Run test suite: 180/188 pass (8 pre-existing unrelated failures)
- [X] T013 Move `ai/features/todos/06-stacked-graph-daily-grouping.md` to `ai/features/done/06-stacked-graph-daily-grouping.md`
- [X] T014 Save AI session summary to `ai/sessions/deepseek-v4-flash-free-032-stacked-graph-daily-grouping-20260710T173500Z.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No tasks — can start immediately
- **Foundational (Phase 2)**: No tasks — can start immediately
- **User Stories (Phase 3+)**: All affect the same file (`payment_reports.html`), so MUST be done sequentially:
  - US1 (Phase 3) must be complete before US2 (Phase 4)
  - US2 (Phase 4) must be complete before US3 (Phase 5)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — start here
- **User Story 2 (P2)**: Depends on US1 — tooltips require stacked chart to exist
- **User Story 3 (P3)**: Depends on US1 and US2 — legend toggle requires stacked chart with tooltips

### Within Each User Story

- All tasks within a US phase affect the same file and must be done in order
- Core rendering before interaction enhancements
- Story complete before moving to next priority

### Parallel Opportunities

- T004 (i18n) in US1 can be done in parallel with T001-T003 (different file: `django.po`)
- T006-T007 in US2 affect only the chart script — no true parallel splits within same file
- T010 (tests) in Polish can run in parallel with UI verification

---

## Parallel Example: User Story 1

```bash
# T004 (i18n) can run in parallel with T001-T003:
Task: "Add i18n key for empty state in django.po"
Task: "Rewrite chart JS in payment_reports.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 (stacked chart + empty state)
2. **STOP and VALIDATE**: Load Reports > Payments and confirm stacked bars render correctly
3. Proceed to US2 and US3 only if time permits

### Incremental Delivery

1. Add User Story 1 → Test independently → Validated (MVP!)
2. Add User Story 2 → Test independently → Validated
3. Add User Story 3 → Test independently → Validated
4. Each story enhances the chart without breaking previous functionality

### Environment Reference

When running commands, use these exact patterns:
- **Run tests**: `docker compose exec web uv run manage.py test`
- **Recompile .mo**: `docker compose exec web uv run manage.py compilemessages`
- **Run lint**: `docker compose exec web uv run ruff check`

---

## Notes

- All user stories modify the same single file (`payment_reports.html`) — sequential execution required
- No backend changes needed — the `PaymentReportView` already returns correct data
- No new JavaScript libraries needed — Chart.js v4 already loaded via CDN
- i18n required for any new user-visible string (empty state message)
- Verify all existing report tests still pass before marking polish complete
