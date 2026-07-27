# Tasks: AI Development Data Collection

**Input**: Design documents from `specs/052-ai-dev-data-collection/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Django backend**: `backend/apps/`, `backend/tests/`
- **Management commands**: `backend/apps/reservations/management/commands/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and context setup

No setup tasks required. This feature uses only Python stdlib modules (`csv`, `pathlib`, `re`, `datetime`) plus existing Django `BaseCommand` — no new libraries, utilities, or dependencies.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites — the `reservations` app already has a `management/commands/` directory with an existing command (`seed_data.py`) to follow as pattern.

---

## Phase 3: User Story 1 — Generate Development Data CSV (Priority: P1) 🎯 MVP

**Goal**: A software quality auditor runs `collect_ai_dev_data` and receives a valid CSV with columns: feature, complexity, minutes, model, start_timestamp, end_timestamp, specs_quality, iterations — populated from `ai/features/done/`, `specs/*/spec.md`, and `ai/sessions/`.

**Independent Test**: Run `docker compose exec web uv run manage.py collect_ai_dev_data --output /tmp/test.csv` after at least one feature is completed through the full Specify→Implement→PR lifecycle. Verify the CSV contains the expected row with correct column values, and that all fields follow the defined rules (complexity in {1,2,3,5,8}, specs_quality in {1..5}, timestamps in ISO 8601).

### Tests for User Story 1

- [X] T001 [P] [US1] Test basic CSV generation produces header + data rows in `backend/tests/test_collect_ai_dev_data.py`
- [X] T002 [P] [US1] Test that rows are generated for all features in `ai/features/done/` in `backend/tests/test_collect_ai_dev_data.py`
- [X] T003 [P] [US1] Test empty state — header only (no data rows) when `ai/features/done/` is empty in `backend/tests/test_collect_ai_dev_data.py`
- [X] T004 [P] [US1] Test graceful handling of malformed session files (missing fields → empty cell, no crash) in `backend/tests/test_collect_ai_dev_data.py`
- [X] T005 [P] [US1] Test complexity values are restricted to {1, 2, 3, 5, 8} in `backend/tests/test_collect_ai_dev_data.py`
- [X] T006 [P] [US1] Test specs_quality values are restricted to {1, 2, 3, 4, 5} in `backend/tests/test_collect_ai_dev_data.py`
- [X] T007 [P] [US1] Test CSV output is RFC 4180 compliant (proper escaping of commas, quotes, newlines) in `backend/tests/test_collect_ai_dev_data.py`

### Implementation for User Story 1

- [X] T008 [US1] Create `collect_ai_dev_data.py` management command skeleton in `backend/apps/reservations/management/commands/collect_ai_dev_data.py` with `BaseCommand`, `add_arguments`, and `handle` entry point
- [X] T009 [US1] Implement feature file parser: scan `ai/features/done/*.md`, extract title from `# ` heading, collect filenames for cross-referencing
- [X] T010 [US1] Implement spec quality assessor: scan `specs/*/spec.md` for section presence to compute `specs_quality` (1–5 scale as defined in spec.md)
- [X] T011 [US1] Implement session log parser: scan `ai/sessions/*.md`, extract `**Model:**`, `**Date:**`, filename timestamps, and command references to compute model, timestamps, minutes, and iterations
- [X] T012 [US1] Implement complexity heuristic: derive complexity (1/2/3/5/8) from session count, iteration count, review cycles, and bug fix mentions across matched sessions
- [X] T013 [US1] Implement CSV writer: assemble rows from parsed data, write to output path using Python stdlib `csv` module with proper RFC 4180 escaping
- [X] T014 [US1] Wire all components together in `handle()`: orchestrate parsing pipeline → assemble CSV → write output

**Checkpoint**: US1 should be fully functional — running `collect_ai_dev_data` produces a valid CSV with populated columns for every completed feature

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification

- [X] T015 Run full test suite: `docker compose exec web uv run pytest` — 279 pass, 7 pre-existing failures
- [X] T016 Validate CSV output against real project data: 40 rows generated with populated columns

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — not applicable (no setup tasks)
- **Foundational (Phase 2)**: No dependencies — not applicable (no blocking prerequisites)
- **User Story 1 (Phase 3)**: Can start immediately
- **Polish (Phase 4)**: Depends on US1 being complete

### User Story Dependencies

- **US1 (P1)**: Single story — no dependencies on other stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Test → Implement → Verify cycle per story
- Implementation order within US1: command skeleton (T008) → feature parser (T009) → spec assessor (T010) → session parser (T011) → complexity (T012) → CSV writer (T013) → wiring (T014)

### Parallel Opportunities

- All tests (T001–T007) are marked [P] and can run in parallel
- T009–T013 can be developed in parallel after T008 (skeleton) is complete, since each parses a different data source or computes an independent column

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test CSV generation with header + data rows in backend/tests/test_collect_ai_dev_data.py"
Task: "Test all features produce rows in backend/tests/test_collect_ai_dev_data.py"
Task: "Test empty state in backend/tests/test_collect_ai_dev_data.py"
Task: "Test malformed session handling in backend/tests/test_collect_ai_dev_data.py"
Task: "Test complexity values in backend/tests/test_collect_ai_dev_data.py"
Task: "Test specs_quality values in backend/tests/test_collect_ai_dev_data.py"
Task: "Test RFC 4180 compliance in backend/tests/test_collect_ai_dev_data.py"

# Implementation — T008 first, then T009–T013 in parallel:
Task: "Create management command skeleton in backend/apps/reservations/management/commands/collect_ai_dev_data.py"
# After T008:
Task: "Implement feature file parser (done/ files)"
Task: "Implement spec quality assessor (specs/ files)"
Task: "Implement session log parser (sessions/ files)"
Task: "Implement complexity heuristic"
Task: "Implement CSV writer"
# Then:
Task: "Wire all components in handle()"
```

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. Complete Phase 3: User Story 1 (tests + implementation)
2. **STOP and VALIDATE**: Test US1 independently
3. Complete Phase 4: Polish (final verification)

### Environment Reference

- **Run management command**: `docker compose exec web uv run manage.py collect_ai_dev_data --output /tmp/ai_dev_data.csv`
- **Run tests**: `docker compose exec web uv run pytest`
- **Run specific tests**: `docker compose exec web uv run pytest backend/tests/test_collect_ai_dev_data.py -v`
- **Lint**: `docker compose exec web uv run ruff check backend/`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No i18n needed — this is a data export CLI tool, not a user-facing web page
- Use Python stdlib only — no external dependencies per spec constraint
