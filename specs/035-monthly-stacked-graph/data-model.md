# Data Model: Monthly Stacked Graph

## Entities

No new entities. Existing `Payment` model is sufficient:

- **Payment.date** — determines which calendar month a payment belongs to.
- **Payment.amount** — aggregated as `Sum('amount')` per month and payment type.
- **Payment.payment_type** — used as segment/dataset key in stacked bar chart.

## Query

No query changes. The existing monthly aggregation uses:

```python
rows = qs.values("date__year", "date__month", "payment_type").annotate(
    total=Sum("amount"), count=Count("id"),
).order_by("date__year", "date__month", "payment_type")
```

Date range filtering via `qs.filter(date__gte=start, date__lte=end)` remains unchanged.
