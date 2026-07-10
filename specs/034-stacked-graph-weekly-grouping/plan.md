# Implementation Plan: Stacked Graph Weekly Grouping

**Branch**: `034-stacked-graph-weekly-grouping` | **Date**: 2026-07-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/034-stacked-graph-weekly-grouping/spec.md`

## Summary

Add a "Week" grouping option to the Reports > Payments stacked bar chart. Each bar represents an ISO week (Monday–Sunday) with Monday-date labels in YYYYMMDD format. Date snapping (start→Monday, end→Sunday) is implemented in the backend `PaymentReportView` before the aggregation query. Builds on the existing daily stacked chart (032-stacked-graph-daily-grouping).

## Technical Context

**Language/Version**: Python 3.12 (Docker), JavaScript (ES6+ in browser)

**Primary Dependencies**: Django 5.x, Chart.js 4 (loaded via CDN in `base.html`)

**Storage**: PostgreSQL — no schema changes required

**Testing**: pytest via `docker compose exec web uv run manage.py test`

**Target Platform**: Linux server (Docker), modern browsers (Chrome, Firefox, Safari)

**Project Type**: Web application — Django monolith with Bootstrap 5.3.3

**Performance Goals**: Chart renders within 1 second on page load; weekly aggregation returns fewer rows than daily, so same or better perf.

**Constraints**: Must reuse existing Chart.js v4 stacked bar implementation from daily grouping feature. No new JavaScript libraries.

**Scale/Scope**: Backend date snapping in `PaymentReportView` + frontend Chart.js adaptation for weekly grouping + tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| i18n (NON-NEGOTIABLE) | ✅ PASS | "Week" dropdown label already exists from prior work; new label "Failed to load chart data." needs i18n key (identified in Phase 1 design) |
| TDD | ✅ PASS | Date snapping tests cover each weekday; chart rendering tests extend daily test pattern |
| Code Quality | ✅ PASS | Lint with ruff via CI; no dead code |
| YAGNI | ✅ PASS | Only modifies existing views/templates/tests; no new models, no new routes |
| Complexity Tracking | ✅ N/A | No complexity additions beyond the feature's core scope |

## Project Structure

### Documentation (this feature)

```text
specs/034-stacked-graph-weekly-grouping/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (changed files)

```text
backend/apps/payments/views.py          # Date snapping in PaymentReportView get_context_data
backend/apps/payments/templates/payments/
└── payment_reports.html                # Chart JS block for weekly grouping

backend/tests/
└── test_payments.py                    # Date snapping tests + weekly chart tests
```

**Structure Decision**: Django monolith. Modified files: view (date snapping logic), template (Chart.js weekly config), tests (snapping + rendering).

## Complexity Tracking

> No complexity additions. Feature reuses existing stacked bar infrastructure with ISO-week date snapping logic.
