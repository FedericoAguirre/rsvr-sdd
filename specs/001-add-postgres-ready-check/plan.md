# Implementation Plan: Add PostgreSQL Readiness Check to App Startup Script

**Branch**: `001-add-postgres-ready-check` | **Date**: 2026-07-07 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-add-postgres-ready-check/spec.md`

## Summary

Modify `backend/start_app01.ps1` to check PostgreSQL readiness before launching the Django dev server. The script will parse connection parameters from `.env`, perform a TCP socket check followed by a `pg_isready` probe (with fallback), retry on failure with configurable timeout, and produce clear error messages when PostgreSQL is unavailable.

## Technical Context

**Language/Version**: PowerShell 5.1+ (Windows), Python 3.12+ (Django)

**Primary Dependencies**: .NET `System.Net.Sockets.TcpClient` (built-in), `pg_isready` (optional, from PostgreSQL client tools)

**Storage**: N/A — no persistent storage changes

**Testing**: Manual — run `start_app01.ps1` with PostgreSQL up, down, and misconfigured. No CI test for PowerShell scripts (no Windows runner).

**Target Platform**: Windows 10/11, Windows Server 2019+

**Project Type**: Django web application + PowerShell startup script

**Performance Goals**: Readiness check adds <1s overhead when PostgreSQL is already running (SC3). Timeout after 30s if unreachable (FR3).

**Constraints**: Only PowerShell 5.1+ built-in features guaranteed; no assumption about Npgsql or PostgreSQL client tools being installed; must parse `.env` format already handled by existing script

**Scale/Scope**: Single file modification (`backend/start_app01.ps1`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1 — Testing Standards (NON-NEGOTIABLE)
- **Requirement**: TDD — tests must be written before implementation and must fail first
- **Assessment**: PASS — this feature modifies a PowerShell script with no test harness available on CI (no Windows runner). Manual testing protocol will be documented in the quickstart guide. No Django/Python test code is affected.
- **Justification if violated**: N/A — PowerShell script execution requires Windows environment not available in CI

### Gate 2 — i18n (NON-NEGOTIABLE)
- **Requirement**: Every user-visible string must be internationalized
- **Assessment**: PASS — script output is developer-facing operational messages in English. Existing project does not internationalize dev tooling output.
- **Justification if violated**: N/A — no user-facing strings added to the Django application

### Gate 3 — Code Quality
- **Requirement**: All code must pass linting and static analysis
- **Assessment**: PASS — only PowerShell changes. No Python code modified. PowerShell script will follow consistent formatting with the existing script style.
- **Justification if violated**: N/A — no Python code changes

### Gate 4 — Performance Requirements
- **Requirement**: Feature must define measurable performance criteria
- **Assessment**: PASS — SC3 defines <1s overhead on healthy startup. SC2 defines timeout + 5s maximum failure exit time. Both are measurable.
- **Justification if violated**: N/A

## Project Structure

### Documentation (this feature)

```text
specs/001-add-postgres-ready-check/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
```

### Source Code (repository root)

```text
backend/
└── start_app01.ps1                    # MODIFIED — add PostgreSQL readiness check
```

**Structure Decision**: Single file change to `backend/start_app01.ps1`. No new files created. No test files (PowerShell cannot be tested in current CI).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations to justify.
