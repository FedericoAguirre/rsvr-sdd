# Implementation Plan: Monthly Stacked Graph

**Branch**: `035-monthly-stacked-graph` | **Date**: 2026-07-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/035-monthly-stacked-graph/spec.md`

## Summary

Add month-boundary date snapping to the existing "Month" grouping in Reports > Payments stacked bar chart. Labels change to YYYYMM format. Start date snaps to the 1st of its month, end date snaps to the last day of its month. Backend logic in `PaymentReportView`, frontend label formatting in `payment_reports.html`.

## Technical Context

**Language/Version**: Python 3.12 (Docker), JavaScript (ES6+ in browser)

**Primary Dependencies**: Django 5.x, Chart.js 4 (loaded via CDN in `base.html`)

**Storage**: PostgreSQL — no schema changes required

**Testing**: pytest via `docker compose exec web uv run manage.py test`

**Target Platform**: Linux server (Docker), modern browsers (Chrome, Firefox, Safari)

**Project Type**: Web application — Django monolith with Bootstrap 5.3.3

**Performance Goals**: Chart renders within 1 second on page load; monthly aggregation returns fewer rows than daily/weekly, same or better perf.

**Constraints**: Must reuse existing Chart.js v4 stacked bar implementation. No new JS libraries. Must reuse existing monthly aggregation query (`date__year`, `date__month`).

**Scale/Scope**: Backend date snapping in `PaymentReportView` + frontend label format change + tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| i18n (NON-NEGOTIABLE) | ✅ PASS | "Month" dropdown label already exists from prior work; no new user-facing strings needed for this feature |
| TDD | ✅ PASS | Date snapping tests (1st/last day, leap year, etc.) extend existing report test pattern |
| Code Quality | ✅ PASS | Lint with ruff via CI; no dead code |
| YAGNI | ✅ PASS | Only modifies existing views/templates/tests; no new models, no new routes |
| Complexity Tracking | ✅ N/A | No complexity additions beyond the feature's core scope |

## Project Structure

### Documentation (this feature)

```text
specs/035-monthly-stacked-graph/
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
└── payment_reports.html                # Label formatting for YYYYMM

backend/tests/
└── test_payments.py                    # Date snapping tests + monthly chart tests
```

**Structure Decision**: Django monolith. Modified files: view (date snapping for month), template (YYYYMM label format), tests (snapping + rendering).

## Complexity Tracking

> No complexity additions. Feature extends existing monthly grouping with date snapping and label formatting, reusing existing stacked bar infrastructure.
