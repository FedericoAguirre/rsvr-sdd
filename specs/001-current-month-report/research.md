# Research: Current Month Payments Report

## Existing Architecture

### View: `PaymentReportView` (`backend/apps/payments/views.py:277`)

- `TemplateView` with `LoginRequiredMixin` and `UserPassesTestMixin`
- Access: superuser or Administrators group
- Accepts GET params: `start`, `end`, `grouping` (day/week/month)
- Fetches payments filtered by date range, grouped with aggregation (Sum + Count)
- Passes `start_date`, `end_date`, `grouping`, `report_data` to template
- When `start`/`end` are empty: no filtering applied (shows all payments regardless of date)

### Template (`backend/apps/payments/templates/payments/payment_reports.html`)

- Form with method GET: date inputs, grouping select, submit button, export button
- Chart.js bar chart rendered from `report_data` JSON injected via `json_script`
- Canvas `totalsChart` renders stacked bars by payment type
- Totals shown as bar labels

### Model: `Payment` (`backend/apps/payments/models.py`)

- Fields: `date` (DateField), `amount` (DecimalField), `payment_type` (CharField choices), `is_deleted` (BooleanField), `client` (FK), `created_by` (FK)
- No new fields or tables needed

## Approach Decision

**Default date range**: Server-side in `PaymentReportView.get_context_data()`
- No NEEDS CLARIFICATION — clear from spec
- When `start` is empty, default to first day of current month
- When `end` is empty, default to last day of current month
- Server-determined month (avoids timezone issues)

**Auto-render**: Implicit via server-side defaults
- Since the page receives `report_data` in initial context, the chart renders immediately on DOM ready
- No additional JS auto-submit needed
- The "automatic trigger" is achieved by the server pre-loading data with defaults

**Manual override**: Existing form behavior unchanged
- User changes dates and clicks "Generate Report"
- Form submits with new params, page reloads with new data

## Edge Cases

| Case | Resolution |
|------|-----------|
| No payments in current month | Empty state message shown by existing template JS logic |
| Manual date fields cleared | View falls back to current month defaults |
| Timezone discrepancy | All dates determined server-side via Django timezone |
| Last day of month boundary | Python's `calendar.monthrange()` returns correct last day |
