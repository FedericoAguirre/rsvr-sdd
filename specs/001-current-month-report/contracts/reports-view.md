# Contract: Payment Reports View

## Endpoint

- **URL**: `GET /payments/reports/`
- **View**: `PaymentReportView`
- **Auth**: LoginRequired + superuser or Administrators group

## Query Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `start` | ISO date (YYYY-MM-DD) | No | First day of current month | Start of date range |
| `end` | ISO date (YYYY-MM-DD) | No | Last day of current month | End of date range |
| `grouping` | string: `day`, `week`, `month` | No | `day` | Aggregation period |

**New behavior**: When `start` and `end` are not provided, defaults to current month boundaries (server-side calculation).

## Response

- **Template**: `payments/payment_reports.html`
- **Context**: `start_date`, `end_date`, `grouping`, `report_data`
- **Content-Type**: `text/html`

## Data Flow

1. Browser navigates to `/payments/reports/` (no params) or submits form with params
2. View reads `start`, `end`, `grouping` from GET
3. If `start`/`end` empty → default to current month boundaries
4. Filter `Payment.objects.filter(date__gte=start, date__lte=end, is_deleted=False)`
5. Group by selected period + payment_type → SUM + COUNT
6. Render template with context + JSON-serialized report_data
7. Chart.js in browser renders stacked bar chart from report_data
