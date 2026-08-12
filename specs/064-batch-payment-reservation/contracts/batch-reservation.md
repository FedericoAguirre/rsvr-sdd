# Batch Reservation Contracts

The feature keeps the existing authenticated JSON endpoints and response shapes.

## `GET /payments/{payment_id}/batch-data/`

Returns:

```json
{
  "payment_id": 123,
  "block_class_count": 5,
  "date_range": {
    "start": "2026-08-11",
    "end": "2026-08-31"
  },
  "equipment_list": [],
  "class_slots": [],
  "reserved_dates": []
}
```

For a payment at August 11, 2026 20:20 with no eligible Tuesday slot remaining, `date_range.start` is `2026-08-12` and `date_range.end` is `2026-09-01`.

## `POST /payments/{payment_id}/batch-create/`

Request body:

```json
{
  "payment_id": 123,
  "equipment_id": 4,
  "class_slot_id": 9,
  "dates": ["2026-08-11", "2026-08-18"]
}
```

The endpoint continues to return `status: "ok"` for complete success, `status: "partial"` with `created` and `failed` details for conflicts, and HTTP 400 with `errors` for invalid input. The new window calculation is enforced during validation, not only in the browser.
