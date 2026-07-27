# Implementation Plan: AI Development Data Collection

**Branch**: `052-ai-dev-data-collection` | **Date**: 2026-07-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/052-ai-dev-data-collection/spec.md`

## Summary

Add a management command that generates a CSV data table from completed AI-assisted feature work. The command reads feature titles from `ai/features/done/`, spec quality from `specs/*/spec.md` files, and session metadata from `ai/sessions/`, then outputs a well-formed CSV with columns: feature, complexity, minutes, model, start_timestamp, end_timestamp, specs_quality, iterations — enabling the software quality auditor to identify bottlenecks and inefficiencies in the SDLC process.

## Technical Context

**Language/Version**: Python 3.12 (Django 5.0)

**Primary Dependencies**: Django 5.0, pytest, psycopg2-binary (existing stack — no new libraries required)

**Storage**: None new — reads from existing flat files (`ai/features/done/*.md`, `ai/sessions/*.md`, `specs/*/spec.md`)

**Testing**: pytest via `docker compose exec web uv run pytest`

**Target Platform**: Linux server (Docker Compose)

**Project Type**: Web application (Django) — feature is a management command within the Django project

**Performance Goals**: CSV generation completes in under 5 seconds for projects with up to 100 completed features. All file I/O is local (no network calls).

**Constraints**:
- Must read from existing directory structures only (no new data sources or schemas)
- Must not modify any existing files during data collection
- Must handle missing, malformed, or empty files gracefully (empty fields instead of failure)
- Must produce RFC 4180-compliant CSV with proper escaping
- Must not introduce new external dependencies — Python stdlib `csv` module is sufficient
- All file reading is read-only; no database queries needed

**Scale/Scope**: Small feature — single management command, file-based data aggregation, CSV output. No new models, views, or templates.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No `.specify/memory/constitution.md` found. Gates derived from project patterns in AGENTS.md and existing specs (051-list-unassociated-reservations).

| Gate | Status | Notes |
|------|--------|-------|
| **I. Code Quality** | ✅ PASS | Single management command; follows existing Django management command conventions; no dead code |
| **II. Testing Standards** | ✅ PASS | pytest tests for command output correctness, edge cases (empty dirs, malformed files), and CSV validity |
| **III. File Handling (Robustness)** | ✅ PASS | All file reads wrapped in try/except per spec FR-007; empty fields instead of crash; no file mutation |
| **IV. Context7 External Docs** | ✅ PASS | Only Python stdlib `csv` module needed — no new external dependencies |
| **V. Performance** | ✅ PASS | All reads are local sequential file I/O; no network or DB queries; runtime dominated by filesystem |

## Project Structure

### Documentation (this feature)

```text
specs/052-ai-dev-data-collection/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
└── apps/
    └── reservations/           # or a new utils app — nearest relevant app for AI data
        └── management/
            └── commands/
                └── collect_ai_dev_data.py   # NEW: management command

backend/tests/
└── test_collect_ai_dev_data.py              # NEW: tests for this feature
```

**Structure Decision**: Django management command within the existing project structure. Command lives under `reservations` app (closest existing app to general utilities) or the existing `utils/` module. Tests placed in `backend/tests/` following the project's flat test directory convention.

## Complexity Tracking

> No constitution violations to justify. Feature is small, single-command, no new models or views.
