# Implementation Plan: Quick Reservation Status Management

**Branch**: `019-quick-reservation-status` | **Date**: 2026-06-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/019-quick-reservation-status/spec.md`

## Summary

Add inline row actions to the reservation list view so operators can mark reservations as "used" or "unused" without navigating to the detail page. Each row will show colored status badges (green=reserved, blue=used, gray=unused) and action buttons that perform the status change via HTMX, updating the row in-place without a full page reload. Reuses the existing `reservation_change_status` view, modified to return an HTMX partial response.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Django, psycopg2-binary, gunicorn, whitenoise, weasyprint, django-htmx (for HTMX request detection)

**Storage**: PostgreSQL 16 (primary), SQLite (development fallback)

**Testing**: pytest 9.1+, pytest-django 4.12+

**Target Platform**: Linux server (Docker/POSIX-compatible)

**Project Type**: Web application (server-rendered Django + HTMX + Bootstrap 5)

**Performance Goals**: Status change reflected visually within 1 second of action. Page load with badges adds no more than 200ms overhead.

**Constraints**: Must coexist with existing redirect-based status change on detail page. Must work without JavaScript disabled (graceful degradation to full page reload).

**Scale/Scope**: Single gym operation, <1000 reservations/day. Feature limited to row-level status changes — no bulk operations.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1 — Code Quality (PASS)
- **Principle**: All code MUST pass automated linting/static analysis (Ruff). No dead code or unresolved TODOs.
- **Impact**: Inline action buttons and badge rendering add new template code and view logic. The existing `reservation_change_status` view will be modified but not replaced. No dead code introduced.
- **Justification**: Straightforward — lint and format with Ruff before merge.

### Gate 2 — Testing Standards — NON-NEGOTIABLE (PASS)
- **Principle**: TDD is mandatory. Tests MUST be written first and reviewed before implementation. Integration tests required for contract changes.
- **Impact**: The `reservation_change_status` view response format changes (adds HTMX partial support). This is a contract change to an existing endpoint — requires integration tests.
- **Justification**: Existing tests in `test_reservations_list.py` cover the detail-page status change flow. New tests will cover the HTMX path: (a) HTMX request returns rendered row partial, (b) non-HTMX request falls back to redirect. Integration tests required.

### Gate 3 — User Experience Consistency (PASS)
- **Principle**: All text MUST be translated (Spanish via i18n). Error messages MUST be actionable. Consistent formatting.
- **Impact**: Button labels, status badge text, and error messages must use `{% translate %}` / `_()`.
- **Justification**: Follow existing patterns in `reservation_detail.html`. All new user-facing strings will be wrapped in translation calls.

### Gate 4 — Performance Requirements (PASS)
- **Principle**: Measurable performance criteria before implementation. Structured logging for observability.
- **Impact**: HTMX partial responses are lighter than full page reloads — performance improves for the status-change action.
- **Justification**: Criteria defined in spec (SC-002: <1 second visual feedback). No significant regression risk.

### Gate 5 — Development Workflow (PASS)
- **Principle**: Specify → Plan → Tasks → Implement cycle. Feature branch sequential numbering. Atomic commits. Each user story independently testable.
- **Impact**: This feature is a single increment (row-level status management). User stories P1+P2 (mark used/unused) are independently testable. P3 (badges) is a prerequisite for P1/P2 from a UX perspective but can be tested independently as a rendering change.
- **Justification**: Branch follows `###-feature-name` convention. All user stories independently testable.

## Project Structure

### Documentation (this feature)

```text
specs/019-quick-reservation-status/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── views.py              # Modify reservation_change_status for HTMX
│       ├── urls.py               # No change (reuse existing route)
│       ├── templates/
│       │   └── reservations/
│       │       ├── reservation_list.html          # Add badges + inline buttons
│       │       ├── reservation_list_by_slot.html  # Add badges + inline buttons
│       │       ├── reservation_detail.html        # No change (existing forms)
│       │       └── partials/
│       │           └── reservation_row.html       # NEW: row partial for HTMX swap
│       └── templatetags/
│           └── reservation_extras.py             # NEW: status badge color filter/tag
└── tests/
    └── test_reservations_list.py   # Add HTMX row operation tests
```

**Structure Decision**: Follow existing Django app structure. Add a `partials/` directory for HTMX partial templates. Add a `templatetags` file if needed for badge color rendering. All modifications are within the existing `reservations` app.

## Complexity Tracking

No complexity violations — this feature reuses existing infrastructure (HTMX is already loaded, status change view already exists) and follows established patterns. YAGNI is respected: no new dependencies, no new database fields, no new routes.

No gate violations requiring justification.
