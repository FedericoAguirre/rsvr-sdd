# Data Model: Current Month Payments Report

## Status: No changes to data layer

This feature is a view-level change only. No new models, fields, columns, or database migrations are required.

### Existing Entities (unchanged)

| Entity | Key Fields | Role |
|--------|-----------|------|
| `Payment` | `date`, `amount`, `payment_type`, `is_deleted` | Source of report data; filtered and aggregated by the view |

### Report Query (view logic only)

- **Input**: `start` (date), `end` (date), `grouping` (day/week/month)
- **Default input**: First and last day of current month (server-side)
- **Aggregation**: `SUM(amount)`, `COUNT(id)` grouped by date period + payment_type
- **Output**: List of dicts with period key, payment_type, total, count → JSON-serialized into template context
