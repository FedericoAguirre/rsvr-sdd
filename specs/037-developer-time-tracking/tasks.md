# Tasks: Developer Time Tracking (CSV Export)

**Input**: Design documents from `/specs/037-developer-time-tracking/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec — manual verification via test fixture repository.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single-file shell script: `scripts/developer-time.sh`
- Test fixtures: `test/fixtures/test-repo.sh`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `scripts/` directory at repository root
- [x] T002 Create `test/fixtures/` directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data extraction infrastructure needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Implement `git log` data extraction in `scripts/developer-time.sh` that captures commit hash, author email, author name, timestamp (epoch), date (YYYY-MM-DD), and file list per commit — output as structured text for pipe processing
- [x] T004 [P] Implement `-o <path>` argument parsing in `scripts/developer-time.sh` with default fallback to `developer-time.csv`
- [x] T005 [P] Implement `--help` flag parsing in `scripts/developer-time.sh` (prints usage and exits 0)
- [x] T006 [P] Implement baseline error handling in `scripts/developer-time.sh`: check `git rev-parse --is-inside-work-tree`, check for commits, print errors to stderr, exit with non-zero code

**Checkpoint**: Foundation ready — git data can be extracted and script validates its environment

---

## Phase 3: User Story 1 - Run CLI Tool to Generate CSV (Priority: P1) 🎯 MVP

**Goal**: The script produces a valid CSV with Developer, Date, Hours, Files Count columns, grouping commits by author email and date.

**Independent Test**: Run against any git repository — CSV output contains headers and one row per developer-date pair.

### Implementation for User Story 1

- [x] T007 [US1] Implement developer-date grouping logic in `scripts/developer-time.sh`: group extracted commits by author_email + date, sorting output chronologically
- [x] T008 [US1] Implement basic hours calculation in `scripts/developer-time.sh`: for each developer-date group, compute hours as (last commit timestamp — first commit timestamp) / 3600 — single-block only, no gap handling yet
- [x] T009 [US1] Implement file count aggregation in `scripts/developer-time.sh`: collect distinct file paths per developer-date group, count them
- [x] T010 [US1] Implement CSV output writer in `scripts/developer-time.sh`: write header row and data rows to the output path specified by `-o`, using comma delimiter, ISO 8601 dates, decimal hours
- [x] T011 [US1] Validate end-to-end: run `scripts/developer-time.sh` against the current repository and verify output CSV has correct headers and row format

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently — a CSV is generated with developer, date, basic hours, and file count

---

## Phase 4: User Story 2 - Accurate Hours Calculation (Priority: P1)

**Goal**: Hours per developer-date account for activity gaps >= 1 hour by splitting into separate work blocks and summing them, rather than using a simple first-to-last range.

**Independent Test**: Create a controlled test repo with known commit timestamps, run the script, and verify hours match the expected multi-block calculation.

### Implementation for User Story 2

- [x] T012 [US2] Implement work block detection in `scripts/developer-time.sh`: within each developer-date group, sort commits by timestamp and identify gaps >= 3600 seconds between consecutive commits — create a new block for each group of commits separated by gaps
- [x] T013 [US2] Implement multi-block hours summation in `scripts/developer-time.sh`: for each work block, compute duration_seconds = (last_commit_seconds — first_commit_seconds), sum across all blocks, convert to decimal hours
- [x] T014 [P] [US2] Create test fixture in `test/fixtures/test-repo.sh`: a script that initializes a temporary git repo with known commit timestamps covering the gap scenarios from spec acceptance criteria (no gap, gap > 1hr, consecutive blocks, past-midnight edge case), plus a verification that expected CSV matches actual output

**Checkpoint**: Hours calculation correctly handles single-block and multi-block days per spec acceptance criteria

---

## Phase 5: User Story 3 - File Change Count (Priority: P2)

**Goal**: Files Count column reflects distinct files changed per developer per date, not total file changes across commits.

**Independent Test**: Run against a repo where a developer modifies the same file multiple times in one day — CSV shows count of 1, not 3.

### Implementation for User Story 3

- [x] T015 [US3] Enhance file tracking in `scripts/developer-time.sh`: replace basic file list aggregation with deduplication by file path per developer-date group (use associative array or sort|uniq approach)
- [x] T016 [US3] Update test fixture in `test/fixtures/test-repo.sh`: add a scenario where the same file is modified multiple times on one date, verify CSV Files Count is 1

**Checkpoint**: File counts are accurate — duplicates and renames do not inflate the count

---

## Phase 6: User Story 4 - Help and Documentation (Priority: P3)

**Goal**: The script has a `--help` flag and inline documentation for team members.

**Independent Test**: Invoking `--help` prints usage text; script works with no arguments.

### Implementation for User Story 4

- [x] T017 [P] [US4] Implement `--help` output text in `scripts/developer-time.sh`: print usage synopsis, argument descriptions (including `-o <path>`), exit codes explanation, and an example invocation — print to stdout and exit 0
- [x] T018 [US4] Update test fixture in `test/fixtures/test-repo.sh`: add test scenario for empty repository (no commits) and single commit (0 hours)
- [x] T019 [US4] Validate edge case — empty repository: run script in a git repo with no commits, verify CSV has headers only or appropriate message
- [x] T020 [US4] Validate edge case — single commit: run script against a repo with exactly one commit, verify hours is 0.0 and file count is 1

**Checkpoint**: Help output is informative, edge cases handled gracefully

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Cross-platform compatibility, performance validation, and final verification

- [x] T021 [P] Cross-platform test: run `scripts/developer-time.sh` on macOS and Linux (or WSL), verify identical CSV output for the same repository — note any `awk`/`date` differences and add compatibility shims if needed
- [x] T022 Performance validation: run against a repository with 10,000+ commits (e.g., the project itself), verify completion in under 30 seconds per FR-010

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 then User Story 2 (US2 builds on hours from US1)
  - User Story 3 depends on US1 (shares the git log extraction pipeline)
  - User Story 4 is independent of US2/US3 — can start after Phase 2
- **Polish (Final Phase)**: Depends on all desired user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 — builds on the hours calculation
- **User Story 3 (P2)**: Can start after US1 — shares git log pipeline
- **User Story 4 (P3)**: Can start after Phase 2 — independent, only touches `--help` and edge cases

### Within Each User Story

- Core implementation before integration
- Story behaves correctly before performance optimization
- Story complete before moving to next priority

### Parallel Opportunities

- All Phase 2 tasks marked [P] can run in parallel (T003-T006 — different concerns: data extraction, argument parsing, help, error handling)
- T014 and T012-T013 can run in parallel (fixture creation vs implementation)
- T017 is independent of T018-T020

---

## Parallel Example: Foundational Phase

```bash
# Launch all Phase 2 tasks in parallel:
Task: "Implement git log data extraction in scripts/developer-time.sh"
Task: "Implement -o argument parsing in scripts/developer-time.sh"
Task: "Implement --help flag in scripts/developer-time.sh"
Task: "Implement baseline error handling in scripts/developer-time.sh"
```

## Parallel Example: User Stories

```bash
# US4 (help/docs) can start alongside US2/US3:
Task: "Implement --help output in scripts/developer-time.sh"  # US4
Task: "Implement multi-block hours in scripts/developer-time.sh"  # US2
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 — basic CSV with hours and file count
4. **STOP and VALIDATE**: Run against any repo, verify CSV output
5. MVP ready — a CSV is generated with meaningful developer activity data

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (data extraction, args, error handling)
2. Add User Story 1 → CSV generated with basic hours → Deploy/Demo (MVP!)
3. Add User Story 2 → Accurate hours with gap handling → Deploy/Demo
4. Add User Story 3 → Distinct file counts → Deploy/Demo
5. Add User Story 4 → Help text and edge case handling → Deploy/Demo

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 + User Story 2 (sequential, builds on same script)
   - Developer B: User Story 4 (independent, just help text and edge cases)
3. After US1 done:
   - Developer A: User Story 2 (hours with gaps)
   - Developer B: User Story 3 (file count)
4. Polish done together

---

## Notes

- [P] tasks = different files, no dependencies on other incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
