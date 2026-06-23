# Implementation Plan: Send Class Reservations Calendar to Client

**Branch**: `021-send-class-calendar` | **Date**: 2026-06-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/021-send-class-calendar/spec.md`

## Summary

Operators need to export a client's class reservation schedule as an ICS calendar file. A date range picker and download button will be added to the existing client detail page (`clients/{pk}/`). A new view at `clients/{pk}/calendar/` accepts start/end date parameters and returns an `.ics` file generated using the `icalendar` Python library. Each reservation becomes a calendar event containing the client name, class slot name, date, and reserved equipment. The filename follows the convention `cal_<client_snake_case>_<start_YYYYMMDD>_<end_YYYYMMDD>.ics`.

## Technical Context

**Language/Version**: Python 3.13, Django 5.0.x

**Primary Dependencies**: `icalendar>=5.0` (new dependency for ICS generation)

**Storage**: PostgreSQL (production), SQLite (development) — no new tables or migrations needed

**Testing**: pytest with pytest-django

**Target Platform**: Web application — Linux/macOS (Docker or uv)

**Project Type**: Web application (Django + PostgreSQL + Bootstrap 5 + HTMX)

**Performance Goals**: ICS file generated in <3 seconds for up to 100 reservations

**Constraints**:
- Timezone must be `America/Denver` (project default)
- No new database migrations required
- All user-facing UI text must be translated to Spanish via Django i18n
- Must support large date ranges (e.g., one year) without timeout

**Scale/Scope**: Single-tenant, small scale (<10k reservations total)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Evaluation

| Gate | Status | Rationale |
|------|--------|-----------|
| I. Code Quality | ✅ PASS | Zero dead code introduced. Adding `icalendar` is justified by the spec. No new complexity beyond required functionality. |
| II. Testing Standards | ✅ PASS | New `icalendar` dependency introduces a contract boundary — integration tests required. TDD cycle will be followed. |
| III. UX Consistency | ✅ PASS | All new UI text (date labels, buttons, error messages) will use Django i18n. Spanish translations added. |
| IV. Performance | ✅ PASS | Success criteria define measurable targets (<3s generation, <3 clicks). |
| Tech Constraints | ✅ PASS | Python 3.13, Django 5.0, opencode — all consistent with existing project. |
| Workflow | ✅ PASS | Sequential numbering (`021-*`), independent user stories, testable increments. |

**No gate violations requiring Complexity Tracking justification.**

## Project Structure

### Documentation (this feature)

```text
specs/021-send-class-calendar/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── client-calendar-download.md
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── clients/
│       ├── templates/clients/
│       │   └── client_detail.html    # [MODIFY] Add date range form + download button
│       ├── urls.py                   # [MODIFY] Add calendar/ route
│       └── views.py                  # [MODIFY] Add client_calendar view
├── config/
│   └── settings.py                   # [MAYBE] Add icalendar to INSTALLED_APPS if needed
├── templates/
│   └── base.html                     # No changes needed
└── tests/
    └── test_client_calendar.py       # [CREATE] Integration tests for ICS download
```

**Structure Decision**: Follow existing Django app structure — add a new view in `apps/clients/views.py`, new route in `apps/clients/urls.py`, modify existing template, create dedicated test file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations to justify. Feature is additive and uses existing patterns.
