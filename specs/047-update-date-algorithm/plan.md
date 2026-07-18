# Implementation Plan: Update Auto-Date Algorithm

**Branch**: `047-update-date-algorithm` | **Date**: 2026-07-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/047-update-date-algorithm/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Change the auto-date algorithm on the reservation create page so that selecting a class slot always sets the date to the same day-of-week in the following week (never the current week). This removes the old time-based edge cases where a future day later this week would select the current week.

## Technical Context

**Language/Version**: Python 3.12, JavaScript (ES5 compatible)

**Primary Dependencies**: Django 5.0.14, Django REST Framework, PostgreSQL

**Storage**: PostgreSQL (via Django ORM)

**Testing**: Django TestCase (unittest-based), `docker compose exec web uv run manage.py test`

**Target Platform**: Linux server (Docker container)

**Project Type**: Django web application with Bootstrap 5 frontend

**Performance Goals**: <500ms page load, date auto-populates within 100ms of class slot selection

**Constraints**: Must maintain backward compatibility with existing reservation data; i18n required for all user-facing strings per constitution

**Scale/Scope**: Small algorithm change in 2 files (JS + Python), test updates. Single developer, single sprint.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | ✅ PASS | No new complexity introduced; algorithm change is a simplification of existing logic |
| II. TDD Mandatory | ✅ PASS | Existing tests exist and will be updated to RED then GREEN |
| III. UX Consistency / i18n | ✅ PASS | No new user-visible strings; existing i18n labels unchanged |
| IV. Performance | ✅ PASS | Same response pattern as existing code |
| Technology Constraints | ✅ PASS | Uses existing Django + JS stack |
| Package Management | ✅ PASS | No new dependencies |
| Workflow | ✅ PASS | Follows standard feature branch workflow |

**All gates pass. No violations to justify.**

## Project Structure

### Documentation (this feature)

```text
specs/047-update-date-algorithm/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── static/reservations/js/auto-date.js    # JS algorithm change
│       ├── templates/reservations/reservation_form.html  # No change needed
│       └── views.py                               # auto_date_for_slot() algorithm change
└── tests/
    └── test_reservations.py                       # Update TestAutoDate assertions
```

**Structure Decision**: Django project — single `backend/` directory with Django apps. All changes confined to `reservations` app and its tests.

## Complexity Tracking

> No complexity additions — this feature simplifies the existing algorithm.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | — | — |
