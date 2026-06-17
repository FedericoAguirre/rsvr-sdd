# Implementation Plan: Filter State Saving

**Branch**: `001-filter-state-saving` | **Date**: 2026-06-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-filter-state-saving/spec.md`

## Summary

Preserve reservation filter form values (class_slot, date, status) across all postback operations on the reservations list page. The filter form uses server-side re-population — submitted GET params are echoed back into the form fields when the response renders. This is a bug fix in the existing `reservation_list` view and template.

## Technical Context

**Language/Version**: Python 3.12+ / Django 5.0.x

**Primary Dependencies**: Django (django>=5.0,<5.1), psycopg2-binary (PostgreSQL adapter), Whitenoise (static files)

**Storage**: PostgreSQL 16

**Testing**: pytest + pytest-django

**Target Platform**: Linux (Docker), POSIX-compatible

**Project Type**: Web application (server-rendered Django templates + Bootstrap 5 + HTMX)

**Performance Goals**: N/A — single-user form interactions; no performance targets needed

**Constraints**: Server-side form re-population from submitted GET/POST params on each postback. All server round-trips from the reservations page preserve filter state. Filter state preserved on all outcomes including errors.

**Scale/Scope**: Internal gym staff (single gym), low volume — <100 reservations/day, <50 class slots, <20 equipment items

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | ✅ Pass | Minimal code changes; existing linting/formatting enforced |
| II. Testing Standards (NON-NEGOTIABLE) | ✅ Pass | TDD will be followed; existing test file `test_reservations_list.py` will be extended |
| III. User Experience Consistency | ✅ Pass | Filter state preservation directly improves UX consistency; error messages use i18n |
| IV. Performance Requirements | ✅ Pass | No performance impact — filter values already in request context |
| Development Workflow | ✅ Pass | Follows Specify → Plan → Tasks → Implement cycle |

**Gate decision**: PASS — proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-filter-state-saving/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── apps/reservations/
│   ├── views.py                    # [MODIFY] reservation_list: fix filter state preservation
│   ├── templates/reservations/
│   │   └── reservation_list.html   # [MODIFY] Add selected attribute for class_slot dropdown
│   └── templatetags/
│       └── reservation_extras.py   # [NO CHANGE]
└── tests/
    └── test_reservations_list.py   # [MODIFY] Add test for filter state preservation
```

**Structure Decision**: Single Django project — modify existing views and templates within `apps/reservations/`. No new files needed.

## Complexity Tracking

> No constitution violations to justify. Feature is a straightforward bug fix with minimal code changes.

## Phase 0: Outline & Research

No unknowns identified in Technical Context. The fix is clear from the spec and codebase analysis:

1. **Root cause**: `reservation_list.html` template renders the `class_slot` `<select>` without a `selected` attribute — it iterates all slots but never marks the current one. The `status` dropdown and `date` input already have value binding logic but may have gaps.
2. **Fix approach**:
   - Add `selected` attribute to the class_slot `<option>` matching the current filter value
   - Verify date field preserves its value across postbacks (currently falls back to `today` when `request.GET.date` is empty)
   - Ensure all three filter fields survive pagination/sorting/other postback actions
3. **Test approach**: Extend `test_reservations_list.py` with tests that submit filter GET params and assert the rendered HTML contains the expected selected values.

### Research Findings

*No formal research needed. Consolidated findings below.*

- **Decision**: Server-side form re-population via template context variables
- **Rationale**: Django's existing request-response cycle naturally supports this — values from `request.GET` are already passed to the template context; only the template needs `selected`/`value` attributes added
- **Alternatives considered**: Client-side sessionStorage, URL query params — rejected because server-side re-population requires zero additional infrastructure and matches the existing pattern

## Phase 1: Design & Contracts

### Data Model

No data model changes. The `Reservation` model and its fields are unchanged. The fix is purely presentational — ensuring filter form controls display the correct selected values after postback.

### Contracts

No external interface changes. The reservations page URL (`GET /reservations/`) already accepts `?class_slot=`, `?date=`, `?status=` query params. These remain unchanged. The fix only affects how the server responds to these params.

### Quickstart

No new commands or setup needed. Existing `docker-compose up` workflow is sufficient.

### Agent Context Update

Update `AGENTS.md` to reference this plan file.

## Phase 2: Tasks

Delegated to `/speckit.tasks`.
