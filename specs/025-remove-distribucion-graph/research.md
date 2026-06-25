# Research: Remove Distribution Graph

## Overview

No research questions needed — the feature scope is fully understood from the spec. This file documents the findings for completeness.

## Target File

- **File**: `backend/apps/payments/templates/payments/payment_reports.html`
- **Chart to remove**: Lines 48-57 (card + canvas `id="distributionChart"`) and lines 107-122 (JavaScript `Chart` instantiation for the pie chart)
- **Layout adjustment**: Change the remaining chart's column from `col-md-6` to `col-12` (line 38)

## Key Findings

| Aspect | Finding |
|--------|---------|
| Backend impact | None — `PaymentReportView` is untouched |
| i18n impact | The `{% translate "Distribution" %}` header is removed with its card; no new strings |
| Test impact | No new tests needed (pure deletion, no new logic) |
| Risk | Low — removing a canvas + script block cannot break the remaining chart |

## Decision

- **Decision**: Remove the Distribution card column and its JS, widen the Totals column to `col-12`
- **Rationale**: Simplest possible change; no backend, data, or test modifications required
- **Alternatives considered**: Hiding via CSS display:none (rejected — dead code); keeping the column empty (rejected — leaves a blank card)
