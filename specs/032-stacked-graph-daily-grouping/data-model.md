# Data Model: Stacked Graph Daily Grouping

**No new data entities.** This feature is a purely presentational change to the payment reports chart. The existing `Payment` model (see `backend/apps/payments/models.py`) already provides:

- `date` — DateField, the time dimension for grouping
- `amount` — DecimalField, the value dimension for bar height
- `payment_type` — CharField (choices: CASH, CC, DC, TRANSF, PAPP), the category dimension for stacking segments

The `PaymentReportView` backend already returns time-grouped aggregation with `payment_type` breakdown. No schema migrations, model changes, or new database queries are required.
