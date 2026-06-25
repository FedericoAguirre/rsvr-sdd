# Implementation Plan: Remove Distribution Graph

**Branch**: `025-remove-distribucion-graph` | **Date**: 2026-06-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/025-remove-distribucion-graph/spec.md`

## Summary

Remove the redundant "Distribution" pie chart (canvas id `distributionChart`) from the payments/reports/ page. The chart is a pie chart that shows the same payment-type breakdown already displayed by the "Totals by Payment Type" bar chart. The fix is a pure template change: delete the second card column and its associated JavaScript block from `payment_reports.html`, then adjust the layout so the remaining bar chart fills the full width.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0+

**Primary Dependencies**: Django, Chart.js (via CDN or static asset)

**Storage**: PostgreSQL (no changes needed — backend data unchanged)

**Testing**: pytest + pytest-django (existing test suite at `backend/tests/test_payments.py`)

**Target Platform**: Linux/macOS server, modern browsers

**Project Type**: Django web application (backend-only template change)

**Performance Goals**: N/A — no measurable performance impact from removing a chart

**Constraints**: N/A — purely presentational change

**Scale/Scope**: Single template file change, no backend modifications

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Before Phase 0**: GATE PASSED — see justifications below.
**After Phase 1**: GATE PASSED — no violations found; design is a pure template deletion with no new logic, no new strings, and no backend changes.

**Testing Standards**: This change is purely presentational (template deletion only). No new business logic is added, so new TDD tests are not required. Existing tests assert the page renders without error. **GATE PASSED** — justification documented in Complexity Tracking.

**i18n Check**: The Distribution card header uses `{% translate "Distribution" %}` — removing the card removes the string. No new strings are introduced, so no i18n violation. **GATE PASSED**.

## Project Structure

### Documentation (this feature)

```text
specs/025-remove-distribucion-graph/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output — no data model changes (empty)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output — no new interfaces
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
└── apps/
    └── payments/
        └── templates/
            └── payments/
                └── payment_reports.html   # Single file to modify
```

**Structure Decision**: Django app template only. No other files need changes.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Skipping TDD for this change | Purely deletion — no logic added, no new testable behavior | Writing a test that asserts "a div is absent" provides no value over visual inspection and would need updating on any layout change |

## Phase 0 — Research

No unresolved questions. The distribution chart is identified at `backend/apps/payments/templates/payments/payment_reports.html:48-57` (card + canvas) and `:107-122` (JavaScript Chart instantiation). The fix is:

1. Remove the second column (`col-md-6`) containing the Distribution card (lines 48-57)
2. Change the remaining column from `col-md-6` to `col-12` (line 38) so the bar chart fills full width
3. Remove the JavaScript block that creates `distributionChart` (lines 107-122)

## Phase 1 — Design & Contracts

### Data Model

No changes. The `PaymentReportView` backend and its data generation remain untouched.

### Contracts

No new interfaces. The existing reports URL, view, and response format are unchanged.

### Quickstart

See [quickstart.md](./quickstart.md).

### Agent Context

Update `AGENTS.md` SPECKIT markers to point at this plan.
