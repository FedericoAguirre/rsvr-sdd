# Implementation Plan: Remove Reservations Dead Code

**Branch**: `017-remove-reservations-dead-code` | **Date**: 2026-06-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/017-remove-reservations-dead-code/spec.md`

## Summary

Remove the redundant `/reservations/list/` endpoint and its dead code (view, template, tests) from the reservations Django app, relocate Export PDF from `/reservations/list/pdf/` to `/reservations/pdf/`, and create a proper migration for the abandoned `updated_by` field on the Reservation model. The main `/reservations/` endpoint remains the canonical list view.

## Technical Context

**Language/Version**: Python >=3.12

**Primary Dependencies**: Django >=5.0,<5.1; WeasyPrint >=62.0

**Storage**: PostgreSQL (via psycopg2-binary)

**Testing**: pytest + pytest-django (DJANGO_SETTINGS_MODULE=config.settings)

**Target Platform**: POSIX (Linux/macOS)

**Project Type**: Web application (Django monolith)

**Performance Goals**: Not applicable — no new code paths added

**Constraints**: Must preserve identical PDF output; no new dependencies; existing tests for retained functionality must pass

**Scale/Scope**: Single Django app (`apps/reservations`) — view removal, URL relocation, migration creation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Code Quality — No dead code committed | ✅ | Feature explicitly removes dead code; linter (Ruff) must pass |
| I. Code Quality — Simplicity / YAGNI | ✅ | Removing redundant endpoint simplifies codebase |
| II. Testing Standards | ✅ | Tests for removed endpoint are removed alongside; remaining tests must pass |
| III. UX Consistency — i18n | ✅ | All user-facing strings already use i18n; no new strings added |
| III. UX Consistency — Documentation | ✅ | PDF export remains functional at new URL; no new docs required |
| IV. Performance Requirements | ✅ | No new code paths; existing performance characteristics unchanged |

**All gates pass.**

## Project Structure

### Documentation (this feature)

```text
specs/017-remove-reservations-dead-code/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (next command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── views.py              # Remove reservation_list_by_slot, relocate reservation_list_pdf
│       ├── urls.py               # Remove list/ route, move pdf/ under reservations/
│       ├── templates/
│       │   └── reservations/
│       │       ├── reservation_list.html        # Update PDF URL reference
│       │       ├── reservation_list_by_slot.html # DELETE
│       │       └── reservation_list_pdf.html    # Keep unchanged
│       └── migrations/
│           ├── 0001_initial.py
│           ├── 0002_alter_reservation_options_and_more.py
│           ├── 0003_reservation_status.py
│           └── 0004_add_updated_by.py           # CREATE (new)
├── tests/
│   └── test_reservations_list.py  # Remove TestClientColumnNoEmail, TestReservationsList; keep rest
└── config/
    └── urls.py                    # Verify reservations/ include is correct
```

**Structure Decision**: Django monolith — unchanged from existing project structure.

## Complexity Tracking

No complexity additions. This feature strictly removes code and adds a single migration.

## Phase 0: Research

No unresolved technical unknowns — all technology choices (Django, pytest, WeasyPrint) are already established in the project. The spec clarifications resolved the two decision points (test removal + migration creation). No research tasks required.

## Phase 1: Design & Contracts

### Data Model

One change: add `updated_by` ForeignKey to Reservation model (nullable, SET_NULL on delete, related_name `updated_reservations`). This was already intended by the abandoned ghost migration.

### Contracts

No external contract changes. The PDF export URL changes internally but the output format (PDF filename, content, Content-Disposition header) remains identical.

### Quickstart

Developer steps for this feature are straightforward — documented in [quickstart.md](./quickstart.md).

### Agent Context

Update AGENTS.md to reference this plan file.
