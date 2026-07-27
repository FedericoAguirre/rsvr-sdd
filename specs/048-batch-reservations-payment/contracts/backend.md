# Contracts: Batch Reservations from Payment

## POST /payments/<id>/batch-create/

Creates N batch reservations for a given payment.

### Request

```json
{
  "payment_id": 42,
  "equipment_id": 7,
  "class_slot_id": 3,
  "dates": ["2026-07-27", "2026-07-28", "2026-07-29"]
}
```

- `dates` must contain exactly N entries where N = payment.class_slot_count
- Each date must be within the allowed range (next Monday + 28 days)
- Each date's day-of-week must match class_slot's day_of_week
- Equipment must be "in service"
- Class slot must be active

### Response (200 — Success)

```json
{
  "status": "ok",
  "created": 3,
  "reservations": [101, 102, 103],
  "failed": []
}
```

### Response (200 — Partial Failure)

```json
{
  "status": "partial",
  "created": 2,
  "reservations": [101, 103],
  "failed": [
    {"date": "2026-07-28", "reason": "already reserved"}
  ]
}
```

### Response (400 — Validation Error)

```json
{
  "status": "error",
  "errors": {
    "dates": ["Must select exactly 3 dates"],
    "equipment_id": ["Equipment is not available"]
  }
}
```

### Response (404)

```json
{
  "status": "error",
  "errors": {"payment_id": ["Payment not found"]}
}
```

## GET /payments/<id>/batch-data/

Returns context data for the batch modal (available dates, equipment, class slots).

### Response

```json
{
  "payment_id": 42,
  "block_class_count": 3,
  "date_range": {
    "start": "2026-07-27",
    "end": "2026-08-24"
  },
  "equipment_list": [
    {"id": 7, "name": "Cinta 1"},
    {"id": 8, "name": "Bicicleta 2"}
  ],
  "class_slots": [
    {"id": 3, "day_of_week": 0, "time": "19:15", "label": "Lunes 19:15"}
  ]
}
```
