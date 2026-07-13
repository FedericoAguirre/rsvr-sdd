# Tasks: Reports Graph Adjustment

**Input**: Design documents from `specs/040-reports-graph-adjustment/`

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

No foundational tasks required — the existing Django app and testing infrastructure are already in place.

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — Full Chart Visibility (Priority: P1) 🎯 MVP

**Goal**: The chart container on the payments reports page is sized so the entire chart (bars, labels, totals) is visible without scrolling.

**Independent Test**: Load `/payments/reports/` and verify that the `#totalsChart` canvas has `height` attribute set to the adjusted value and the `.card-body` container has `max-height` style that keeps the chart within viewport.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [US1] Test: canvas height attribute is set to adjusted value (e.g., `250`) in `backend/tests/test_payments.py`
- [x] T002 [P] [US1] Test: chart container does not exceed viewport when data is present in `backend/tests/test_payments.py`

### Implementation for User Story 1

- [x] T003 [US1] Adjust canvas `height` from `300` to `250` in `backend/apps/payments/templates/payments/payment_reports.html`
- [x] T004 [US1] Add `max-height` and `overflow-y` styles to `.card-body` containing the chart in `backend/apps/payments/templates/payments/payment_reports.html`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T005 Run all tests pass: `docker compose exec web uv run pytest tests/test_payments.py -v`
- [x] T006 Verify existing chart rendering still works (no regression)
- [x] T007 Save AI session file in `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — already complete
- **Foundational (Phase 2)**: No dependencies — already complete
- **User Story 1 (Phase 3)**: Can start immediately
- **Polish (Phase 4)**: Depends on US1 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — can start immediately

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation then makes tests pass
- Story complete before moving to next priority

### Parallel Opportunities

- T001 and T002 (US1 tests) can run in parallel
- T003 and T004 (US1 implementation) must run sequentially (same file)

---

## Parallel Example: User Story 1

```bash
# Launch tests for User Story 1:
Task: "T001 Test canvas height attribute"
Task: "T002 Test chart container viewport fit"

# Launch implementation after tests fail:
Task: "T003 Adjust canvas height in template"
Task: "T004 Add max-height to card-body"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 — chart height adjustment
2. **STOP and VALIDATE**: Test US1 independently
3. Deploy/demo if ready

### Environment Reference

- **Run tests**: `docker compose exec web uv run pytest`
- **Run specific test**: `docker compose exec web uv run pytest tests/test_payments.py -v -k <test_name>`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- No new dependencies, no schema changes — purely template/CSS
