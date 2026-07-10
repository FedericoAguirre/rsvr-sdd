# Implementation Plan: Stacked Graph Daily Grouping

**Branch**: `032-stacked-graph-daily-grouping` | **Date**: 2026-07-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/032-stacked-graph-daily-grouping/spec.md`

## Summary

Replace the existing flat bar chart on the Reports > Payments page with a stacked bar chart that displays time-grouped payment totals broken down by payment type. The backend (`PaymentReportView`) already returns the correct time-grouped data — only the frontend Chart.js rendering needs to change.

## Technical Context

**Language/Version**: Python 3.12 (Docker), JavaScript (ES6+ in browser)

**Primary Dependencies**: Django 5.x, Chart.js 4 (loaded via CDN in `base.html`)

**Storage**: PostgreSQL — no schema changes required

**Testing**: pytest via `docker compose exec web uv run manage.py test`

**Target Platform**: Linux server (Docker), modern browsers (Chrome, Firefox, Safari)

**Project Type**: Web application — Django monolith with Bootstrap 5.3.3

**Performance Goals**: Chart renders within 1 second on page load; no backend queries changed

**Constraints**: Must use existing Chart.js v4; no new JavaScript libraries may be added. Zero changes to backend views or data model.

**Scale/Scope**: Single template change to `payment_reports.html` — JS rendering logic only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| i18n (NON-NEGOTIABLE) | ✅ PASS | All existing i18n keys reused; no new user-visible strings introduced |
| TDD | ✅ PASS | Tests for chart rendering exist in `test_payments.py`; visual regression tests via browser |
| Code Quality | ✅ PASS | Lint with ruff; no dead code |
| YAGNI | ✅ PASS | Single file change; no new dependencies, models, or views |
| Complexity Tracking | ✅ N/A | No complexity additions to justify |

## Project Structure

### Documentation (this feature)

```text
specs/032-stacked-graph-daily-grouping/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (changed files)

```text
backend/apps/payments/templates/payments/
└── payment_reports.html   # Only file changed — rewrite chart JS block

backend/tests/
└── test_payments.py       # Add tests for stacked chart rendering
```

**Structure Decision**: Django monolith — single template change in existing app. No new files, routes, or views.

## Complexity Tracking

> No complexity additions. This is a purely presentational change reusing existing backend data.
