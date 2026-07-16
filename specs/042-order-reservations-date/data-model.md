# Data Model: Order Reservations by Date in Payment Detail

**Feature**: `042-order-reservations-date` | **Date**: 2026-07-14

## Status

No schema changes. All entities exist. This feature only changes the query ordering on an existing view.

## Existing Entities (for context)

### Reservation

Represents a booked class session. Defined in `backend/apps/reservations/models.py`.

| Field | Type | Notes |
|-------|------|-------|
| `id` | PK | Auto-generated |
| `date` | DateField | The date of the class — primary sort field |
| `class_slot` | ForeignKey → ClassSlot | Provides the time used for secondary sort |
| `client` | ForeignKey → Client | |
| `equipment` | ForeignKey → Equipment | |
| `status` | CharField | Choices: reserved, used, unused |

**Meta.ordering**: `["-date", "class_slot__time"]` (but this only applies when querying Reservation directly).

### PaymentReservation (Through Model)

Links payments to reservations. Defined in `backend/apps/payments/models.py`.

| Field | Type | Notes |
|-------|------|-------|
| `id` | PK | Auto-generated |
| `payment` | ForeignKey → Payment | Related name: `payment_reservations` |
| `reservation` | ForeignKey → Reservation | Related name: `payment_links` |
| `created_at` | DateTimeField | Auto-set on creation |

No `Meta.ordering` — default is PK order.

### ClassSlot (for secondary sort)

| Field | Type | Notes |
|-------|------|-------|
| `id` | PK | |
| `day_of_week` | IntegerField | 0=Monday through 4=Friday |
| `time` | TimeField | e.g., 17:30, 18:30 |

## Query Path

```
Payment → payment_reservations (PaymentReservation) → reservation (Reservation) → class_slot (ClassSlot)
```

Sorting traverses: `-reservation__date`, `-reservation__class_slot__time`

## Validation Rules

- Reservations without an associated class slot fall back to date-only sorting (any stable order within same date).
- No constraints change — this is a presentation-only change.
