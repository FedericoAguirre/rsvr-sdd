# Implementation Plan: CSV Client Upload

**Branch**: `016-csv-client-upload` | **Date**: 2026-06-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/016-csv-client-upload/spec.md`

## Summary

Allow Operators to upload a CSV file to create and update client records. The system parses the CSV, matches rows against existing clients by name/email/mobile, creates new clients for unmatched rows, and displays a results summary with counts of processed, created, updated, and errored records.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Django 5.0, Python `csv` module (stdlib), Bootstrap 5.3, HTMX

**Storage**: PostgreSQL 16

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker)

**Project Type**: Web application (Django server-rendered templates)

**Performance Goals**: Process 1,000 CSV rows and return results within 10 seconds

**Constraints**: Server-rendered Django templates. CSV parsing uses Python stdlib `csv` module (no third-party CSV library). File upload size limit of 5 MB.

**Scale/Scope**: Internal gym management system, <10,000 client records. File uploads up to 1,000 rows per batch.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment | Details |
|-----------|------------|---------|
| I. Code Quality | ✅ Pass | Linting (Ruff) enforced. New CSV parsing logic is self-contained. |
| II. Testing Standards | ✅ Pass | TDD applicable. Integration tests needed for CSV upload → DB flow. |
| III. UX Consistency | ✅ Pass | Upload page follows existing Django form patterns. Error/summary messages must use i18n Spanish. |
| IV. Performance | ✅ Pass | Performance target defined (1,000 rows / 10s). No new external dependencies. |
| Technology Constraints | ✅ Pass | Uses Python stdlib `csv` — no new dependencies. |
| Development Workflow | ✅ Pass | Feature branch exists. |

**Gate verdict**: Pass — no constitutional violations.

## Project Structure

### Documentation (this feature)

```text
specs/016-csv-client-upload/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── clients/
│       ├── models.py                # Client model (existing, no changes needed)
│       ├── forms.py                 # Add CSV upload form
│       ├── views.py                 # Add CSV upload view + processing logic
│       ├── urls.py                  # Add upload URL pattern
│       ├── csv_import.py            # New: CSV parsing, matching, and processing logic
│       └── templates/
│           └── clients/
│               ├── client_csv_upload.html     # New: upload form page
│               └── _client_csv_results.html   # New: results summary partial
└── tests/
    └── test_client_csv_upload.py    # New: tests for CSV upload feature

ai/
└── sessions/       # compressed session files per constitution
```

**Structure Decision**: Existing Django app structure. CSV import logic lives in a dedicated `csv_import.py` module to keep views clean and testable.

## Complexity Tracking

> No complexity violations — this is a self-contained feature using Python stdlib with no new dependencies or architectural changes.
