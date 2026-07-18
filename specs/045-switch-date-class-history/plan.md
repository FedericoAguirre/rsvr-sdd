# Implementation Plan: Switch date and class block columns in history

**Branch**: `045-switch-date-class-history` | **Date**: 2026-07-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/045-switch-date-class-history/spec.md`

## Summary

Reorder the "Historial de Reservas" table columns on the `clients/{id}/` page from Date/Class/Equipment to Class/Date/Equipment. This is a single-file template change with no new models, views, or dependencies.

## Technical Context

**Language/Version**: Python 3.11 / Django 4.2 (existing)

**Primary Dependencies**: Django templates (existing) — no new dependencies required

**Storage**: N/A (no data changes)

**Testing**: pytest via `docker compose exec web uv run pytest` (existing)

**Target Platform**: Linux server (Docker deployment)

**Project Type**: Web application (Django)

**Performance Goals**: N/A — template rendering only, no measurable performance impact

**Constraints**: i18n compliance — existing `{% translate %}` tags must be reused; TDD mandatory per constitution

**Scale/Scope**: Single template file change (`backend/apps/clients/templates/clients/client_detail.html`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Code Quality | ✅ Pass | No new code; template reorder only |
| II. Testing (TDD) | ✅ Pass | Tests must be written FIRST and fail before template change |
| III. UX / i18n | ✅ Pass | Existing `{% translate %}` tags reused; no new strings |
| IV. Performance | ✅ Pass | No measurable performance impact |
| Development Workflow | ✅ Pass | Sequential branch numbering; atomic commits |

**No violations to justify.** Complexity Tracking section is not needed.

## Project Structure

### Documentation (this feature)

```text
specs/045-switch-date-class-history/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # N/A — no external interfaces
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── clients/
│       └── templates/
│           └── clients/
│               └── client_detail.html    # Single file change
└── tests/
    └── test_client_detail.py              # TDD test file
```

**Structure Decision**: Web application (Django) — single template file change in existing app structure.
