# Quickstart: Stacked Graph Weekly Grouping

## Prerequisites

- Docker running (`docker compose up -d`)
- Feature branch `034-stacked-graph-weekly-grouping`

## What to Implement

### 1. Backend — Date Snapping (`backend/apps/payments/views.py`)

In `PaymentReportView.get_context_data()`, before the grouping logic:

- Parse `start`/`end` from GET params
- If `grouping == "week"`:
  - Snap `start` to closest preceding Monday: `start -= timedelta(days=start.weekday())`
  - Snap `end` to closest following Sunday: `end += timedelta(days=6 - end.weekday())`
  - Store snapped dates back in `context["start_date"]` and `context["end_date"]`
- No changes to the existing `qs.extra(...)` week query

### 2. Frontend — Weekly Chart Config (`backend/apps/payments/templates/payments/payment_reports.html`)

Add a `grouping === "week"` branch alongside the existing `"day"` and `"month"` branches:

- X-axis: `type: 'category'` with labels in YYYYMMDD format
- Same dataset structure (payment type segments) from `report_data`
- Tooltip: same `payment type, total, count` format
- Datalabels plugin: same total-on-top-of-bar from daily config
- Grid lines: same responsive config

### 3. i18n

Add key for `"Failed to load chart data."` in the Django locale files.

### 4. Tests (`backend/tests/test_payments.py`)

- Test date snapping for each weekday (Monday–Sunday) for both start and end
- Test that existing `grouping=week` endpoint returns expected data shape
- Test empty state for zero-result ranges

## Run Tests

```bash
docker compose exec web uv run manage.py test
```

## Refs

- Existing daily chart: `specs/032-stacked-graph-daily-grouping/`
- View: `backend/apps/payments/views.py` (lines 199–235)
- Template: `backend/apps/payments/templates/payments/payment_reports.html`
