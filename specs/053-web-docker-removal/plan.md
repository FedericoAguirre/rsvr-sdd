# Implementation Plan: Remove Docker for Web Development, Keep Database

**Branch**: `053-web-docker-removal` | **Date**: 2026-07-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/053-web-docker-removal/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Remove the `web` Docker service from `docker-compose.yml` so the Django application runs natively via `uv run manage.py runserver` while the PostgreSQL database remains in Docker. Update all developer tooling (Makefile, setup script, README, environment config) to support the new hybrid local + Docker workflow.

## Technical Context

**Language/Version**: Python 3.12+ (Django 5.0.x)

**Primary Dependencies**: uv (package manager), Docker Compose (database only), PostgreSQL 16 Alpine

**Storage**: PostgreSQL 16 (runs in Docker container, data persisted via Docker volume)

**Testing**: pytest (test suite), ruff (linting/formatting)

**Target Platform**: macOS/Linux developer machines (Windows via WSL/Git Bash as secondary)

**Project Type**: Web application (Django)

**Performance Goals**: Dev server starts in under 5 seconds, hot-reload under 2 seconds, full setup from clean checkout under 3 minutes

**Constraints**: Pre-deployment Docker stack must remain functional; existing tests must pass with identical results; database state must remain reproducible across machines

**Scale/Scope**: Single environment transformation — no application code changes, no data model changes, no CI/CD changes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1 — Development Environment Mandate (Constitution Section: Development Environment & Package Management)

**Violation**: The constitution states *"All backend tasks, test executions, and database migrations MUST be executed inside the container"* and *"Always use uv via the system environment inside Docker (UV_SYSTEM_PYTHON=true)"*. This feature intentionally moves all backend tasks, tests, and migrations out of the container to run natively on the host.

**Justification Required**: This is the core purpose of the feature — eliminating Docker overhead for the development loop. The constitution's Docker mandate was written when full containerization was the workflow. The feature replaces it with a hybrid model (local app + Docker database) that is explicitly documented as the new constitution-compliant workflow. The Development Environment section of the constitution should be updated as part of this feature to reflect the new hybrid approach.

### Gate 2 — Internationalization (Constitution Principle III — NON-NEGOTIABLE)

**No violation**: The strings affected by this feature are:
- `setup.sh` output messages (developer tooling, not application UI)
- `Makefile` help text (developer tooling)
- `README.md` updates (documentation)

All changes are in developer tooling and documentation, not in application code that renders to end users. The i18n requirement targets application UI strings visible to customers. Developer tooling output does not go through Django's i18n system and adding translation infrastructure to shell scripts is not practical. The constitution's i18n requirement applies to Django application code (templates, views, forms) — this feature touches none of those.

### Gate 3 — External Documentation & Dependency Integrity (Constitution Principle V)

**No violation**: Any code written against library/framework APIs in implementation must use Context7 MCP. This feature primarily modifies configuration files (docker-compose.yml, Makefile, .env.example, setup.sh, README.md) — none of which involve library/framework API calls that would require Context7 lookups. If the implementation phase touches Django settings, Django documentation should be fetched via Context7.

### Gate 4 — Code Quality (Constitution Principle I)

**No violation**: All code changes must pass linting and static analysis. The feature introduces no Python code changes — only configuration and shell script changes. Shell scripts (setup.sh) and Makefile follow standard conventions.

### Gate 5 — Testing Standards (Constitution Principle II — NON-NEGOTIABLE)

**No violation**: All existing tests must pass with identical results when run via `make test` (pytest). The feature does not change any application logic that would alter test behavior. Test results should be verified both locally and via the pre-deployment Docker stack.

### Gate 6 — Performance (Constitution Principle IV)

**No violation**: Success criteria define measurable performance targets (setup < 3 min, server start < 5 s, hot-reload < 2 s) that are documented in the spec and tracked in the implementation.

**Result**: GATE 1 requires explicit justification (tracked in Complexity Tracking below). All other gates pass without violations.

## Project Structure

### Documentation (this feature)

```text
specs/053-web-docker-removal/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
/ (repository root)
├── docker-compose.yml        # Remove web service, keep db service
├── Makefile                  # Replace Docker targets with local dev targets
├── setup.sh                  # NEW: bootstrap script
├── .env.example              # Add DATABASE_URL with localhost
├── README.md                 # Replace Docker setup with local dev instructions
├── backend/
│   ├── pyproject.toml        # Unchanged
│   ├── config/settings.py    # Unchanged (reads DATABASE_URL from env)
│   └── ...                   # No application code changes
```

**Structure Decision**: Single project with Django backend. All changes are at repository root level — no new source files, only configuration and documentation changes. The setup.sh script is the only new file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Constitution Development Environment mandate (Gate 1) | Docker introduces significant I/O latency, hot-reload delays, and IDE debugger friction on local dev machines. Moving to native execution is the purpose of the feature. | Keeping full Docker and using docker exec for all tasks was the old approach. Adding file sync tools (docker-sync, mutagen) adds complexity without solving the core issue. Pure Docker is still available via `make docker-up` for pre-deployment testing. |
| i18n (Gate 2 — partial concern) | Makefile help text and setup.sh output messages are in English (consistent with existing developer tooling in the project). These are not application UI strings and are not rendered to end users through Django templates. | Adding i18n infrastructure to shell scripts and build configuration is disproportionate to the value — no Django template changes are involved. |
