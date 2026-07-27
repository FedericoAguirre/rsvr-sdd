# Implementation Plan: Calendar Downloading in Reservations Page

**Branch**: `050-calendar-downloading-reservations` | **Date**: 2026-07-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/050-calendar-downloading-reservations/spec.md`

## Summary

Add a "Download Calendar" button to the reservations list page that generates and serves an ICS file containing all reservations in the selected date range, with each event description including the payment identifier. The ICS generation logic will be extracted into a shared utility reused across clients, payments, and reservations apps.

## Technical Context

**Language/Version**: Python 3.12 (Django 5.0)

**Primary Dependencies**: Django 5.0, icalendar, pytest, Bootstrap 5.3, HTMX 2.x

**Storage**: PostgreSQL (existing)

**Testing**: pytest via `docker compose exec web uv run pytest`

**Target Platform**: Linux server (Docker Compose)

**Project Type**: Web application (Django)

**Performance Goals**: ICS generation < 200ms for typical date ranges (up to 100 reservations)

**Constraints**: 
- Must reuse/extract existing `_generate_ics` pattern from clients app
- ICS timezone: America/Denver
- Event duration: 1 hour per reservation
- All user-visible strings must be internationalized (i18n)

**Scale/Scope**: Small feature — one new view, one new URL, one button in template, shared utility extraction

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **I. Code Quality** | ✅ PASS | No dead code; refactor `_generate_ics` into shared utility to eliminate duplication |
| **II. Testing Standards** | ✅ PASS | Red-Green-Refactor: tests before implementation, integration test for ICS generation |
| **III. UX Consistency (i18n)** | ✅ PASS | All new strings (button, labels, empty state) must use `{% translate %}` / `gettext` |
| **IV. Performance** | ✅ PASS | ICS generation is on-demand (not on page load); no performance regression expected |
| **V. External Docs** | ✅ PASS | Fetch icalendar docs via Context7 MCP before writing ICS generation code |

## Project Structure

### Documentation (this feature)

```text
specs/050-calendar-downloading-reservations/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 — research artifacts
├── data-model.md        # Phase 1 — entity definitions
├── quickstart.md        # Phase 1 — development quickstart
├── contracts/           # Phase 1 — interface contracts
└── tasks.md             # Phase 2 — implementation tasks (generated later)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   ├── reservations/
│   │   ├── views.py              # Add calendar view, shared utility import
│   │   ├── urls.py               # Add calendar/ route
│   │   └── templates/
│   │       └── reservations/
│   │           └── reservation_list.html  # Add "Download Calendar" button
│   ├── clients/
│   │   └── views.py              # Refactor _generate_ics into shared utility
│   └── payments/
│       └── views.py              # Refactor inline ICS to use shared utility
├── utils/
│   └── ical.py                   # NEW: shared ICS generation utility
└── tests/
    ├── test_reservations_calendar.py  # NEW: calendar download tests
    └── test_ical_utils.py             # NEW: shared utility tests
```

**Structure Decision**: Django web application — single backend project with app-based separation.

## Complexity Tracking

> No constitution violations to justify. Feature is small and straightforward.
