# Batch Reservation Interface Contract

## `GET /payments/{payment_id}/batch-data/`

The existing authenticated endpoint remains unchanged.

Response fields used by the modal:

```json
{
  "payment_id": 123,
  "block_class_count": 3,
  "date_range": {
    "start": "2026-08-12",
    "end": "2026-09-01"
  },
  "equipment_list": [],
  "class_slots": [
    {"id": 1, "day_of_week": 1, "time": "19:15:00", "label": "19:15:00"}
  ],
  "reserved_dates": ["2026-08-19"]
}
```

Date-grid rules:

- `date_range.start` and `date_range.end` are inclusive ISO calendar dates.
- Each date's weekday is calculated from the ISO date, with Monday as position `0`.
- `reserved_dates` are omitted from selectable cells but do not change the weekday position of other dates.
- The response does not need new weekday or layout fields.

## `POST /payments/{payment_id}/batch-create/`

The existing authenticated JSON payload remains unchanged:

```json
{
  "payment_id": 123,
  "equipment_id": 4,
  "class_slot_id": 1,
  "dates": ["2026-08-12", "2026-08-19", "2026-08-26"]
}
```

The `dates` array contains the exact ISO dates represented by selected date buttons. The alignment change must not transform, reorder, or shift these values.

Existing validation and error response behavior remains authoritative for invalid JSON, invalid dates, wrong date counts, duplicate dates, out-of-window dates, unavailable class slots, and payment-day cutoff violations.
