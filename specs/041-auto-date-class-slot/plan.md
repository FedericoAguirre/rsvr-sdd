# Implementation Plan: Auto-set Date on Class Slot Selection

**Branch**: `041-auto-date-class-slot` | **Date**: 2026-07-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/041-auto-date-class-slot/spec.md`

## Summary

Add client-side JavaScript to the reservation create form that auto-calculates and sets the date field when a class slot is selected, based on day-of-week and time rules.

## Technical Context

**Language/Version**: Python 3.13 / Django 5.0 (backend); JavaScript (client-side)

**Primary Dependencies**: None new — vanilla JS, Django form widgets (existing)

**Storage**: PostgreSQL 16 (existing — no schema changes)

**Testing**: pytest (backend); manual JS testing or in-browser verification

**Target Platform**: Web browser (desktop)

**Project Type**: Web application (Django template-based backend)

**Performance Goals**: Date auto-populates within 1 second of class slot selection

**Constraints**: No new dependencies; date input must support `type="date"` for native picker; JS must handle day-of-week mapping (0=Monday..4=Friday)

**Scale/Scope**: Single template change (`reservation_form.html`) + optional static JS file

## Constitution Check

| Gate | Status | Rationale |
|------|--------|-----------|
| **Code Quality** | ✅ Pass | Small JS addition; linting via ruff unaffected |
| **Testing Standards (TDD)** | ✅ Pass | Tests for calculation logic via Python unit tests + in-browser verification |
| **UX / i18n** | ✅ Pass | No new user-facing strings; existing i18n preserved |
| **Performance** | ✅ Pass |JS runs on interaction only — negligible overhead |
| **Dev Environment** | ✅ Pass | All work inside Docker; no new dependencies |
| **Governance** | ✅ Pass | Standard workflow; single template + optional static file |

**No violations — Complexity Tracking not required.**

## Project Structure

### Documentation (this feature)

```text
specs/041-auto-date-class-slot/
├── plan.md              # This file
├── research.md          # Phase 0 — existing form structure analysis
├── data-model.md        # Phase 1 — no schema changes
├── quickstart.md        # Phase 1 — implementation steps
├── contracts/
│   └── auto-date.md     # Phase 1 — JS contract for the auto-date function
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── templates/
│       │   └── reservations/
│       │       └── reservation_form.html  # Add JS for auto-date logic
│       └── static/
│           └── reservations/
│               └── js/
│                   └── auto-date.js       # New file: auto-date calculation
└── tests/
    └── test_reservations.py               # Add tests for auto-date logic
```

**Structure Decision**: Django app `reservations` — template modification + new static JS file + tests.

## Complexity Tracking

> Not required — no constitution violations to justify.
