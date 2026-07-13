# Implementation Plan: Reports Graph Adjustment

**Branch**: `040-reports-graph-adjustment` | **Date**: 2026-07-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/040-reports-graph-adjustment/spec.md`

## Summary

Adjust the Chart.js chart container height on the payments reports page so the full chart (bars, labels, totals) is visible without scrolling — a pure CSS/template change.

## Technical Context

**Language/Version**: Python 3.13 / Django 5.0 (template: HTML + Bootstrap 5 + Chart.js)

**Primary Dependencies**: Chart.js (CDN-loaded via template), Bootstrap 5 (existing — no new dependencies)

**Storage**: N/A — no data-level changes

**Testing**: pytest + django-test (docker compose exec web uv run pytest) — visual verification via rendered HTML

**Target Platform**: Web browser (desktop, tablet)

**Project Type**: Web application (Django template-based backend)

**Performance Goals**: No impact — zero runtime cost, CSS-only change

**Constraints**: Must not break existing chart rendering; must work at 768px+ viewport width

**Scale/Scope**: Single template change — `backend/apps/payments/templates/payments/payment_reports.html`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Rationale |
|------|--------|-----------|
| **Code Quality** | ✅ Pass | Minimal CSS-only change; linting via ruff (Python) unaffected |
| **Testing Standards (TDD)** | ✅ Pass | Visual feature — testable via HTML content assertions on canvas container attributes |
| **UX / i18n** | ✅ Pass | No new user-facing strings; existing i18n preserved |
| **Performance** | ✅ Pass | CSS-only, zero runtime overhead |
| **Dev Environment** | ✅ Pass | All work inside Docker; no new dependencies |
| **Governance** | ✅ Pass | Standard workflow; single template change with atomic commit |

**No violations — Complexity Tracking not required.**

## Project Structure

### Documentation (this feature)

```text
specs/040-reports-graph-adjustment/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — existing template analysis
├── data-model.md        # Phase 1 output — no schema changes
├── quickstart.md        # Phase 1 output — implementation steps
├── contracts/
│   └── reports-view.md  # Phase 1 output — UI contract
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       └── templates/
│           └── payments/
│               └── payment_reports.html  # Adjust chart container height / canvas sizing
└── tests/
    └── test_payments.py  # Add test for chart container dimensions
```

**Structure Decision**: Single Django app (`payments`) — only `payment_reports.html` template needs modification.

## Complexity Tracking

> Not required — no constitution violations to justify.
