# Data Model: Associated Reservations Calendar Download

## Entities

No new models or database changes are required. All entities already exist.

### Payment (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| client | ForeignKey(Client) | The client this payment is for |
| payment_identifier | CharField | Unique, auto-generated (e.g., EF20260721001) |
| date | DateField | Payment date |
| class_slot_count | PositiveSmallIntegerField | Number of block classes paid |

### PaymentReservation (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| payment | ForeignKey(Payment) | FK to payment, related_name=`payment_reservations` |
| reservation | OneToOneField(Reservation) | Unique — each reservation linked to at most one payment |

### Reservation (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| client | ForeignKey(Client) | Related via `client` FK |
| equipment | ForeignKey(Equipment) | Reserved equipment |
| class_slot | ForeignKey(ClassSlot) | Class slot with day-of-week and time |
| date | Date | Reservation date |
| status | CharField | reserved / used / unused |

### Client (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| name | CharField | Client full name (converted to snake_case for filename) |

## Relationships

```
Payment (1) ──< PaymentReservation >── (1) Reservation
                                        │
                                        ├── (1) Equipment
                                        ├── (1) ClassSlot
                                        └── (1) Client
```

## Query Pattern

The calendar download view will query:

```python
payment.payment_reservations.select_related(
    "reservation__client",
    "reservation__equipment",
    "reservation__class_slot",
).order_by("reservation__date", "reservation__class_slot__time")
```

This is identical to the existing query in `PaymentDetailView.get_context_data()`.
