# URL Route Contracts: Payments Module

## Route Table

| Method | URL Pattern | View Name | Permission | Description |
|--------|-------------|-----------|------------|-------------|
| GET | `/payments/` | `payments:list` | Operator | Paginated payment list (all clients) |
| GET | `/payments/client/{client_id}/` | `payments:client_history` | Operator | Paginated history for one client (5 per page) |
| GET | `/payments/create/` | `payments:create` | Operator | New payment form |
| POST | `/payments/create/` | `payments:create` | Operator | Submit new payment |
| GET | `/payments/{id}/` | `payments:detail` | Operator | Payment detail view |
| GET | `/payments/{id}/edit/` | `payments:edit` | Operator | Edit payment (reference, notes, evidence only) |
| POST | `/payments/{id}/edit/` | `payments:edit` | Operator | Submit edit |
| POST | `/payments/{id}/delete/` | `payments:delete` | Operator | Soft-delete payment |
| GET | `/payments/reports/` | `payments:reports` | Admin | Payment reports view |
| POST | `/payments/{id}/associate/` | `payments:associate` | Operator | Associate payment with reservations |
| GET | `/payments/from-reservation/` | `payments:create_from_reservation` | Operator | Create payment from New Reservations page |

## Template Context Contracts

### payment_list.html
- `payments`: Paginated queryset of Payment objects
- `page_obj`: Django paginator page
- `client_filter`: Optional client ID if filtering

### payment_form.html
- `form`: Payment ModelForm instance
- `payment_types`: List of available payment types
- `mode`: "create" or "edit"
- `payment`: Optional existing Payment instance (for edit mode)
- `from_reservation`: Boolean — true if creating from New Reservations page
- `client_id`: Optional pre-selected client ID

### payment_reports.html
- `report_data`: JSON-serializable dict with aggregated data
- `grouping`: "day" | "week" | "month" | "range"
- `start_date`, `end_date`: Date range for the report
- `chart_data`: JSON data for Chart.js (labels, datasets)
