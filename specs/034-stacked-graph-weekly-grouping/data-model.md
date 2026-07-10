# Data Model: Stacked Graph Weekly Grouping

**No new data entities.** The existing `Payment` model (see `backend/apps/payments/models.py`) already provides:

- `date` — DateField, the time dimension for ISO week grouping
- `amount` — DecimalField, the value dimension for bar height
- `payment_type` — CharField (choices: CASH, CC, DC, TRANSF, PAPP), the category dimension for stacking segments

## Changes to Existing Logic

### Date Snapping (View Layer, not Model)

The `PaymentReportView.get_context_data()` gains date snapping before the aggregation query:

- **Start date** → snap backwards to closest preceding Monday via `date.weekday()` arithmetic
- **End date** → snap forwards to closest following Sunday via `date.weekday()` arithmetic
- Snapped dates update the form input fields (FR-002, FR-003)

### Query

The existing weekly aggregation query uses PostgreSQL `date_trunc('week', date)` which returns ISO weeks starting on Monday — no change needed to the query itself.
