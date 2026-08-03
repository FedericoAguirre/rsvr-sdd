# Tasks: Fix ClassPrice Demarcation on New Price Entry

**Input**: Design documents from `specs/062-fix-classprice-demarcation/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Test tasks included — existing tests must be updated to match new behavior, and new tests must cover acceptance scenarios.

**Organization**: Single user story (P1) — bug fix with no new infrastructure needed.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)

---

## Phase 1: User Story 1 - Admin adds a new price, previous prices are automatically archived (Priority: P1) 🎯 MVP

**Goal**: When a new class price is entered via `enter_price()`, all existing `current=True` records are archived (`current=False`, `changed_at=timezone.now()`, `changed_by=changed_by`) before the new price is created.

**Independent Test**: Create an initial price, add a second price, verify the first is no longer "Current" and has `changed_at`/`changed_by` populated. Only one record with `current=True` exists after the operation.

### Implementation for User Story 1

- [x] T001 [US1] Add `from django.utils import timezone` import in `backend/apps/classes/models.py`
- [x] T002 [US1] Update `ClassPrice.enter_price()` classmethod in `backend/apps/classes/models.py` to bulk-update all existing `current=True` records to `current=False`, `changed_at=timezone.now()`, `changed_by=changed_by` before creating the new price
- [x] T003 [US1] Update existing tests in `backend/tests/test_classes_classprice.py` that assert `enter_price()` does NOT archive previous prices (lines referencing "no swap/retire" behavior) to match the new archiving behavior
- [x] T004 [US1] Add new test cases in `backend/tests/test_classes_classprice.py` covering acceptance scenarios: first price (no archiving), second price (single archive), multiple legacy current prices (bulk archive), and transaction atomicity
- [x] T005 Run `backend/.venv/bin/pytest backend/tests/test_classes_classprice.py -v` to verify all tests pass

**Checkpoint**: `enter_price()` correctly archives previous current prices. The price history page shows exactly one "Current" record, and all inactive records have populated `changed_at`/`changed_by` fields.

---

## Phase 2: Polish & Validation

- [x] T006 Run full test suite: `backend/.venv/bin/pytest -v` from `backend/` directory to confirm no regressions
- [x] T007 Validate via quickstart.md scenarios (manual walkthrough or automated shell verification)

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 1)**: No dependencies — can start immediately
- **Polish (Phase 2)**: Depends on Phase 1 completion

### Within User Story 1

- T001 (import) → T002 (fix) — sequential, same file
- T003 (update existing tests) → can run in parallel with T001/T002
- T004 (new tests) → depends on T002 (needs the fixed method)
- T005 (run tests) → depends on T002, T003, T004

### Parallel Opportunities

- T001 + T003 can start simultaneously (different files: models.py vs test file)
- T004 can be drafted in parallel with T002 if the expected behavior is clear

---

## Parallel Example: User Story 1

```bash
# Start these together:
Task: "T001 Add import in backend/apps/classes/models.py"
Task: "T003 Update existing tests in backend/tests/test_classes_classprice.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001 → T002: Fix the `enter_price()` method
2. Complete T003 → T004: Update and add tests
3. Complete T005: Verify all tests pass
4. Complete T006 → T007: Full suite + quickstart validation
5. **DONE** — deploy/demo

### Environment Reference

- **Run tests**: `docker compose exec web pytest backend/tests/test_classes_classprice.py -v`
- **Full test suite**: `docker compose exec web pytest -v`
- **Rebuild after changes**: `docker compose up -d --build web`

---

## Notes

- No schema changes, no migrations needed — all fields already exist
- The fix is ~3 lines added to `enter_price()` (import + filter/update call)
- Existing tests that assert "no swap/retire" behavior will need assertion updates
- Quickstart.md contains shell-based validation scenarios (Scenario 4) that can be run directly
