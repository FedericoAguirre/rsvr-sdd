---

description: "Task list for updating the Windows auto-start deployment documentation"

---

# Tasks: Update Restart Docs

**Input**: Design documents from `specs/030-update-restart-docs/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Test tasks are included per FR-007 (TDD required by constitution).

**Organization**: Tasks are grouped by user story. Per TDD, test tasks must be written and fail before implementation begins.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation**: `docs/windows11_deployment.md` (modified)
- **Tests**: `backend/tests/test_restart_docs.py` (new)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Read current docs and understand existing structure

- [x] T001 Read current `docs/windows11_deployment.md` `## Start the App After Restart` section (lines 295–343) to understand existing Option 1, 2, 3 content
- [x] T002 Read `backend/tests/test_payments_associate_button.py` as reference for test conventions (pytest fixtures, Django test client patterns, naming)

**Checkpoint**: Current state understood — ready to implement changes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Understand the target PowerShell commands that will appear in the docs

- [x] T003 Validate the PowerShell `.env` loader command syntax: `Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }` works correctly with comment lines, blank lines, and values containing `=`
- [x] T004 Validate that `uv run .\manage.py runserver` is the correct command for the project (check `manage.py` and `pyproject.toml` in `backend/`)

**Checkpoint**: PowerShell commands validated — ready for TDD test writing and doc implementation

---

## Phase 3: User Story 1 - Update Auto-Start Documentation (Priority: P1) 🎯 MVP

**Goal**: Update `docs/windows11_deployment.md` so all three startup options use consistent PowerShell .env loading + `uv run .\manage.py runserver` instead of `cmd.exe` / `waitress-serve`.

**Independent Test**: Open the rendered markdown — each option should include a PowerShell code block with the env loader pattern and `uv run .\manage.py runserver`.

### Tests for User Story 1 (TDD — write FIRST, ensure FAIL before implementation)

> **NOTE: Write these tests FIRST, ensure they FAIL (docs still use cmd.exe/waitress-serve), then implement.**

- [x] T005 [P] [US1] Create `backend/tests/test_restart_docs.py` with imports and module structure (pytest, pathlib for reading docs/)
- [x] T006 [P] [US1] Write test that extracts PowerShell code blocks from `docs/windows11_deployment.md` and asserts at least one contains the `.env` loader pattern `SetEnvironmentVariable`
- [x] T007 [P] [US1] Write test that extracts `uv run` command from the docs and validates it references `manage.py runserver`

**Expected to FAIL** at this point (docs still use `cmd.exe` + `waitress-serve`)

### Implementation for User Story 1

- [x] T008 [US1] Update Option 3 (Auto-Start Using Task Scheduler) in `docs/windows11_deployment.md` to use `powershell.exe -Command` with inline env loader + `uv run .\manage.py runserver` instead of `cmd.exe` / `waitress-serve`
- [x] T009 [US1] Update Option 1 (Manual Start) in `docs/windows11_deployment.md` to use PowerShell env loader + `uv run .\manage.py runserver` instead of `waitress-serve`
- [x] T010 [P] [US1] Update Option 2 (Launcher Script) in `docs/windows11_deployment.md` to use a `.ps1` wrapper with the PowerShell env loader + `uv run .\manage.py runserver` pattern
- [x] T011 [US1] Add security note to `docs/windows11_deployment.md` in the `## Start the App After Restart` section advising `icacls .env /inheritance:r /grant "Administrators:R"` to restrict `.env` file permissions and warning that Task Scheduler stores commands in plain text
- [x] T012 [US1] Verify all three options are internally consistent (same env loader pattern, same `uv run` command, correct `D:\Descargas\codigo\rsvr-sdd` path resolution)

**Checkpoint**: Docs updated — all three options now use PowerShell + `uv run`. The test tasks (T005–T007) should NOW PASS after linting.

---

## Phase 4: User Story 2 - Add Test Method Validation (Priority: P2)

**Goal**: The test method in `backend/tests/test_restart_docs.py` fully validates that the documentation PowerShell commands are syntactically correct and that relative paths resolve properly.

**Independent Test**: Run `pytest backend/tests/test_restart_docs.py -v` — all tests pass; no Windows/PowerShell execution required.

### Implementation for User Story 2

- [x] T013 [P] [US2] Add test that validates the `.env` loader regex filters out comments (`#`) and blank lines, and correctly parses `KEY=VALUE` pairs (including values containing `=`)
- [x] T014 [US2] Add test that validates the project path `D:\Descargas\codigo\rsvr-sdd` resolves to a valid directory structure containing `backend/manage.py` (relative path validation)
- [x] T015 [US2] Add test that validates the test itself does NOT attempt to execute PowerShell or start the server (assert no `subprocess.run` or `os.system` calls)

**Checkpoint**: Full test suite passes — all 5+ tests validate docs content without execution.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup and final verification

- [x] T016 Run `ruff check backend/tests/test_restart_docs.py` to confirm zero lint errors (9 D102 remaining — matches existing test convention)
- [x] T017 Verify `docs/windows11_deployment.md` renders correctly (no broken markdown, code blocks properly fenced)
- [x] T018 Run `pytest backend/tests/test_restart_docs.py -v` to confirm all tests pass
- [x] T019 Commit all changes and verify branch is clean

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — read docs to establish baseline
- **Foundational (Phase 2)**: Depends on Setup — validate PowerShell commands
- **User Story 1 (Phase 3)**: Depends on Setup + Foundational
  - Tests (T005–T007) MUST be written first and FAIL before implementation (T008–T012)
- **User Story 2 (Phase 4)**: Depends on Phase 3 tests existing (extends test file)
- **Polish (Phase 5)**: Depends on all user stories complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Check PowerShell syntax before writing docs
- Verify consistency across all three options
- Run tests after implementation to confirm they now PASS

### Parallel Opportunities

- T001 and T002 (Setup) can run in parallel
- T005, T006, T007 (US1 tests) can run in parallel
- T009 and T010 (Options 1 and 2) can run in parallel (different parts of same file)
- T013, T014, T015 (US2 tests) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all US1 tests together (TDD — write first, expect failure):
pytest backend/tests/test_restart_docs.py -v --tb=short

# Launch Options 1 and 2 updates together:
# (edit docs/windows11_deployment.md Option 1 section)
# (edit docs/windows11_deployment.md Option 2 section)

# Run all tests after implementation:
pytest backend/tests/test_restart_docs.py -v
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (read existing docs)
2. Complete Phase 2: Foundational (validate commands)
3. Complete Phase 3: User Story 1 (write tests → implement docs)
4. **STOP and VALIDATE**: Run `pytest backend/tests/test_restart_docs.py -v` — all pass
5. MVP delivered: docs updated, tests validate the content

### Incremental Delivery

1. Setup + Foundational → Baseline ready
2. Write failing tests (T005–T007) → Red phase confirmed
3. Update Option 3 (T008) → Tests start passing for Option 3
4. Update Options 1 and 2 (T009, T010) → All tests pass (Green)
5. Add security note (T011) → Documentation complete
6. Add US2 validation tests (T013–T015) → Extended coverage
7. Polish → Final verification

### Notes

- [P] tasks = different files or independent edits, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable
- TDD: verify tests fail before implementing docs
- Commit after each logical block
- Tests require NO Windows or PowerShell execution — pure static analysis
