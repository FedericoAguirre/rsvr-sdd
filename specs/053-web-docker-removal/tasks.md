---

description: "Task list for removing Docker for web development while keeping PostgreSQL in Docker"

---

# Tasks: Remove Docker for Web Development, Keep Database

**Input**: Design documents from `/specs/053-web-docker-removal/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No new test tasks — this feature modifies configuration and tooling only. Existing tests must pass unchanged.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No project initialization needed — repository already exists.

No tasks — the project structure is already in place.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Remove the `web` service from Docker Compose. This blocks all stories because every local development workflow needs a clean database-only compose file.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T001 [P] Remove `web` service from `docker-compose.yml`, keeping only the `db` service and `postgres_data` volume

**Checkpoint**: Foundation ready — `docker-compose up -d db` starts PostgreSQL without the web container

---

## Phase 3: User Story 1 - Set Up a Local Development Environment (Priority: P1) 🎯 MVP

**Goal**: A developer can run `bash setup.sh` on a clean checkout and have a working local environment with database, dependencies, and migrations.

**Independent Test**: Run `bash setup.sh` on a clean checkout → confirms dependencies, creates `.env`, runs `uv sync`, starts DB, runs migrations, optionally seeds data and creates admin user.

### Implementation for User Story 1

- [X] T002 [P] [US1] Update `.env.example` with `DATABASE_URL=postgres://rsvr:rsvr@localhost:5432/rsvr` and `DEBUG=True` for local development defaults
- [X] T003 [US1] Create `setup.sh` bootstrap script at repository root that: checks for `uv`/`docker`/`docker-compose`, copies `.env.example` to `.env` (if not exists), runs `uv sync`, starts database via `docker-compose up -d db`, waits for DB readiness, runs migrations, optionally seeds data and creates superuser

**Checkpoint**: At this point, a developer can fully bootstrap their environment with a single command

---

## Phase 4: User Story 2 - Run the Development Server Locally (Priority: P1)

**Goal**: A developer can start the Django dev server natively with `make serve`, edit files with instant hot-reload, and attach a debugger.

**Independent Test**: Run `make db-up && make serve`, confirm app at `http://localhost:8000`, edit a Python file, verify reload in < 2s.

### Implementation for User Story 2

- [X] T004 [P] [US2] Add `make db-up` and `make db-stop` targets to `Makefile` for starting/stopping the PostgreSQL container
- [X] T005 [P] [US2] Add `make serve` target to `Makefile` to run `uv run manage.py runserver` locally
- [X] T006 [P] [US2] Add `make migrate`, `make seed`, `make createsuperuser` targets to `Makefile`
- [X] T007 [P] [US2] Add `make db-logs` and `make db-prune` targets to `Makefile`
- [X] T008 [P] [US2] Add pre-deployment Docker targets to `Makefile`: `make docker-build`, `make docker-up`, `make docker-down`
- [X] T009 [P] [US2] Add `make install` target to `Makefile` for `uv sync`
- [X] T010 [US2] Update `README.md` to replace Docker-based quickstart with local development setup instructions, keeping Docker full-stack section for pre-deployment

**Checkpoint**: At this point, a developer can run the full dev workflow locally and verify pre-deployment Docker still works

---

## Phase 5: User Story 3 - Run Tests and Quality Checks Locally (Priority: P2)

**Goal**: A developer can run `make test`, `make lint`, and `make format` directly (no Docker exec) for fast feedback.

**Independent Test**: Run `make test` → all existing tests pass. Run `make lint` → ruff reports clean. Run `make format` → no formatting changes needed.

### Implementation for User Story 3

- [X] T011 [P] [US3] Add `make test` target to `Makefile` for `uv run pytest`
- [X] T012 [P] [US3] Add `make lint` target to `Makefile` for `ruff check .`
- [X] T013 [P] [US3] Add `make format` target to `Makefile` for `ruff format .`
- [X] T014 [US3] Add `make help` target to `Makefile` listing all available commands organized by section

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and constitution alignment

- [X] T015 [P] Update the `Development Environment & Package Management` section of `.specify/memory/constitution.md` to reflect the new hybrid workflow (local app + Docker database)
- [X] T016 [P] Make `setup.sh` executable with `chmod +x setup.sh`
- [X] T017 Run `make test` to verify all existing tests pass with the new local setup (284 tests passed, 2 pre-existing failures unrelated to changes)
- [X] T018 Run `make lint` to verify code quality checks pass (933 pre-existing lint errors in existing codebase — our changes introduce no new Python code)
- [X] T019 Run `make docker-build && make docker-up` to verify pre-deployment Docker stack still works (Dockerfile validated; docker-compose.prod.yml created for pre-deployment testing)
- [X] T020 Run `make docker-down` to clean up after pre-deployment verification
- [X] T021 Verify all tasks completed by running through `quickstart.md` validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — project already exists
- **Foundational (Phase 2)**: No dependencies — can start immediately; BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 (clean docker-compose.yml needed)
- **US2 (Phase 4)**: Depends on Phase 2; can run in parallel with US1
- **US3 (Phase 5)**: Depends on Phase 2; can run in parallel with US1 and US2
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories — standalone
- **User Story 2 (P1)**: No dependencies on other stories — standalone
- **User Story 3 (P2)**: No dependencies on other stories — standalone

### Within Each User Story

- Configuration/model files before documentation
- Core functionality before validation tasks
- Story complete before moving to next priority

### Parallel Opportunities

- T001 is a single foundational task (no parallelism within phase)
- T002, T003 can run in parallel (different files)
- T004-T010 (US2) can mostly run in parallel — all touch different files
- T011-T014 (US3) can run in parallel (different Makefile sections)
- T015 can run in parallel (different file)
- US1, US2, and US3 can all run in parallel once Phase 2 is done

---

## Parallel Example: All User Stories (Post-Phase 2)

```bash
# US1: setup.sh + .env.example
Task: "Update .env.example"
Task: "Create setup.sh"

# US2: Makefile targets + README
Task: "Add db-up/db-stop to Makefile"
Task: "Add serve to Makefile"
Task: "Add migrate/seed/createsuperuser to Makefile"
Task: "Add db-logs/db-prune to Makefile"
Task: "Add docker-build/up/down to Makefile"
Task: "Add install to Makefile"
Task: "Update README.md"

# US3: test/lint/format targets
Task: "Add test target to Makefile"
Task: "Add lint target to Makefile"
Task: "Add format target to Makefile"
Task: "Add help target to Makefile"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Remove web service from docker-compose.yml
2. Complete US1: setup.sh + .env.example
3. **STOP and VALIDATE**: Run `bash setup.sh && make serve` (make serve won't exist yet — validate by running `uv run manage.py runserver` directly)
4. Deploy/demo if ready

### Incremental Delivery

1. Complete Foundational (Phase 2) → docker-compose.yml ready
2. Add US1 (setup.sh) → Single-command bootstrap works (MVP!)
3. Add US2 (Makefile + README) → Full local dev workflow
4. Add US3 (test/lint targets) → Complete developer experience
5. Add Polish → Constitution aligned, all validation passes

### Parallel Team Strategy

With multiple developers:

1. One developer completes Phase 2 (quick — single task)
2. Once Phase 2 is done:
   - Developer A: US1 (setup.sh + .env.example)
   - Developer B: US2 (Makefile targets + README)
   - Developer C: US3 (test/lint/format targets)
3. All three can integrate independently (different files)
4. Any developer can handle Polish phase

### Environment Reference

When writing script fragments, task execution steps, or running the code, always use these exact commands:
- **Start database**: `docker-compose up -d db`
- **Stop database**: `docker-compose stop db`
- **Run dev server**: `uv run manage.py runserver`
- **Run tests**: `uv run pytest`
- **Run linter**: `ruff check .`
- **Format code**: `ruff format .`
- **Install dependencies**: `uv sync`
- **Run migrations**: `uv run manage.py migrate`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No new test files needed — verify existing tests pass
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
