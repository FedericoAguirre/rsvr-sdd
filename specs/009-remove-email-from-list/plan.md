# Implementation Plan: Remove Email from Client Column in Reservations List

**Branch**: `009-remove-email-from-list` | **Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/009-remove-email-from-list/spec.md`

## Summary

Remove email addresses from the client name column in all three reservations list views (full list, by-slot, PDF export) by replacing `{{ r.client }}` with explicit first/last name fields in the templates. Keep `Client.__str__` unchanged.

## Technical Context

**Language/Version**: Python 3.12, Django 5.0.x

**Primary Dependencies**: Django template engine, weasyprint (PDF)

**Storage**: PostgreSQL 16 (no schema changes)

**Testing**: pytest + pytest-django, `django.test.Client`

**Target Platform**: Linux (Docker), macOS (dev)

**Project Type**: Web application (Django + PostgreSQL)

**Performance Goals**: No performance impact — pure template change

**Constraints**: Must NOT modify `Client.__str__`; must handle missing first/last names without leading/trailing whitespace

**Scale/Scope**: 3 template files, ~3-4 new view-level tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Code Quality** — ✅ Simple template change, passes linting, no dead code
- **II. Testing Standards (NON-NEGOTIABLE)** — ⚠️ **Gate**: Tests must be written FIRST (TDD). New view-level tests must verify email is absent from client column in all 3 list views. Tests must fail before implementation.
- **III. User Experience Consistency** — ✅ Client column label already uses `{% translate "Client" %}` (Spanish: "Cliente"). No new i18n strings needed.
- **IV. Performance Requirements** — ✅ No performance impact. No new endpoints or queries.

**Gate result**: PASS (tests will be written before implementation per TDD)

**Post-design re-check**: ✅ All gates still pass. Design adds a small `full_name` template filter — sandboxed, testable, no model changes, no schema impact.

## Project Structure

### Documentation (this feature)

```text
specs/009-remove-email-from-list/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (no data model changes)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (no contracts needed)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       └── templates/
│           └── reservations/
│               ├── reservation_list.html          # MODIFY
│               ├── reservation_list_by_slot.html  # MODIFY
│               └── reservation_list_pdf.html      # MODIFY
└── tests/
    └── test_client_column_no_email.py             # CREATE (or add to existing test file)
```

**Structure Decision**: Web application. Only template files and test files are touched.
