# Implementation Plan: Consistent Reservations List

**Branch**: `016-consistent-reservations-list` | **Date**: 2026-06-20 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/015-consistent-reservations-list/spec.md`

## Summary

Fix the reservations list view so that the same set of columns (Date, Client, Class Slot, Equipment, Status, View button) is displayed consistently on page load, after applying a filter, and after clearing a filter. The bug is in the Django template `reservation_list.html` which renders different table headers depending on whether a class_slot filter is active — the filtered view shows only Equipment/Client/Status instead of all six columns. No backend changes are required.

## Technical Context

**Language/Version**: Python 3.12+ (Django 5.0.x)

**Primary Dependencies**: Django 5.0, Bootstrap 5.3.3, HTMX 2.0.4, WeasyPrint 62.0

**Storage**: PostgreSQL 16 via Django ORM

**Testing**: pytest 9.1 + pytest-django 4.12

**Target Platform**: Linux (Docker Debian-slim) / macOS (local dev)

**Project Type**: Server-rendered web application (Django)

**Performance Goals**: Page load time must not increase by more than 5% vs current baseline (SC-003)

**Constraints**: Export PDF functionality must remain unchanged (FR-004)

**Scale/Scope**: Internal gym management tool; low user count

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Code Quality**: No new code dependencies; linting enforced via Ruff. ✅
- **II. Testing Standards (NON-NEGOTIABLE)**: TDD required. Tests must be written and reviewed first, fail before implementation. New tests needed for consistent column display. ✅
- **III. User Experience Consistency**: The feature directly addresses UX inconsistency. Any new UI text/headers must use i18n. ✅
- **IV. Performance Requirements**: SC-003 defines measurable criterion (<5% page load increase). ✅
- **Technology Constraints**: Django + PostgreSQL within existing stack. ✅
- **Development Workflow**: Single feature branch (016-consistent-reservations-list). ✅
- **No complexity violations** — the fix is a template change with no new abstractions, dependencies, or projects.

## Project Structure

### Documentation (this feature)

```text
specs/015-consistent-reservations-list/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (empty — no external API contracts)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── templates/
│       │   └── reservations/
│       │       └── reservation_list.html   # FIX: unify table columns for filtered/unfiltered states
│       └── views.py                        # No changes needed
├── templates/
│   └── base.html                           # No changes needed
└── tests/
    └── test_reservations_list.py           # ADD: tests for consistent column display
```

**Structure Decision**: Django web application with standard MVT layout. The fix is confined to a single template (`reservation_list.html`) with corresponding tests added to the existing test file.

## Complexity Tracking

N/A — no constitution violations. The fix is a straightforward template change with no new abstractions, dependencies, or projects.
