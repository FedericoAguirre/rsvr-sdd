# Batch Reservation Interface Contract

## `GET /payments/{payment_id}/batch-data/`

The authenticated endpoint keeps its existing response shape:

```json
{
  "payment_id": 26,
  "block_class_count": 5,
  "date_range": {
    "start": "2026-08-31",
    "end": "2026-09-25"
  },
  "equipment_list": [],
  "class_slots": [],
  "reserved_dates": []
}
```

Contract rules:

- `date_range.start` remains the first eligible date from the existing algorithm.
- `date_range.end` is inclusive and extends far enough for 20 Monday-through-Friday dates from `start`.
- `reserved_dates` remains client-specific and does not alter the calculated business window.
- `class_slots` and all other response fields retain their current names and meanings.

## `POST /payments/{payment_id}/batch-create/`

The JSON payload remains unchanged:

```json
{
  "payment_id": 26,
  "equipment_id": 1,
  "class_slot_id": 2,
  "dates": ["2026-08-31", "2026-09-01"]
}
```

The form continues to validate exact dates against the extended inclusive range, selected class-slot weekday/time, payment-day cutoff, duplicate dates, permissions, conflicts, and existing quantity rules.
