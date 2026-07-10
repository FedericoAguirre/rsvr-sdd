# Tasks: Remove Custom Range

**Input**: Design documents from `/specs/033-remove-custom-range/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/payments/`, `backend/tests/`, `backend/locale/`
- Paths adjusted for Django monolith structure

---

## Phase 1: Setup (Shared Infrastructure)

No tasks. No new infrastructure required.

---

## Phase 2: Foundational (Blocking Prerequisites)

No tasks. No blocking prerequisites.

**Checkpoint**: Ready for user story implementation.

---

## Phase 3: User Story 1 — Dropdown no longer shows "Custom Range" (Priority: P1) 🎯 MVP

**Goal**: Remove the "Custom Range" option from the "Group by" dropdown and delete all associated backend code. Gracefully fall back to month grouping for any `?grouping=range` requests.

**Independent Test**: Load Reports > Payments and confirm the dropdown has exactly three options: Day, Week, Month. Visit `/payments/reports/?grouping=range` and confirm it renders with month grouping (no error).

### Implementation for User Story 1

- [X] T001 [P] [US1] Remove "Custom Range" `<option>` from the dropdown in `backend/apps/payments/templates/payments/payment_reports.html`
- [X] T002 [P] [US1] Remove the `elif grouping == "range":` block from `PaymentReportView` in `backend/apps/payments/views.py`
- [X] T003 [P] [US1] Remove "Custom Range" i18n entry from `backend/locale/es/LC_MESSAGES/django.po` and recompile `.mo`
- [X] T004 [US1] Update test `test_reports_day_grouping_with_date_range` in `backend/tests/test_payments.py` — remove `grouping=range` specific assertions or update to use a valid grouping

**Checkpoint**: At this point, User Story 1 should be fully functional — dropdown has 3 options, backend ignores `range`, tests pass.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification.

- [X] T005 Run test suite: 12/12 report tests pass (180/188 total, 8 pre-existing unrelated failures)
- [X] T006 Save AI session summary to `ai/sessions/deepseek-v4-flash-free-033-remove-custom-range-20260710T181500Z.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No tasks
- **Foundational (Phase 2)**: No tasks
- **User Story 1 (Phase 3)**: Can start immediately — all T001-T004 are independent (different files)
- **Polish (Phase 4)**: Depends on US1 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — start here

### Within Each User Story

- T001, T002, T003, T004 all touch different files and can run in parallel
- T001: template only
- T002: view only
- T003: locale files only
- T004: test file only

### Parallel Opportunities

- T001, T002, T003, T004 can all be executed simultaneously (4 different files, no overlap)

---

## Parallel Example: User Story 1

```bash
# Run all 4 tasks in parallel:
Task: "Remove dropdown option in payment_reports.html"
Task: "Remove elif range block in views.py"
Task: "Remove i18n entry in django.po and recompile"
Task: "Update test in test_payments.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: All 4 tasks in parallel
2. **STOP and VALIDATE**: Run report tests, verify dropdown

### Environment Reference

When running commands, use these exact patterns:
- **Run tests**: `docker compose exec web uv run pytest -v -k "report"`
- **Recompile .mo**: `docker compose exec web uv run manage.py compilemessages`

---

## Notes

- All 4 US1 tasks modify different files — can be done in any order or parallel
- The `range` grouping is functionally identical to `day` (confirmed in research.md)
- Date range inputs (`start`/`end`) remain functional for remaining groupings
