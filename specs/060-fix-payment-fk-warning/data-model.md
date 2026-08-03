# Data Model: Fix PaymentReservation ForeignKey Warning

## Entity: PaymentReservation

**Purpose**: Join record linking a `Payment` to a `Reservation` with a one-to-one constraint. Each reservation belongs to at most one payment.

### Fields (Changed)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `payment` | `ForeignKey(Payment)` | `on_delete=CASCADE`, `related_name="payment_reservations"` | Unchanged |
| `reservation` | `OneToOneField(Reservation)` | `on_delete=CASCADE`, `related_name="payment_links"` | **Changed** from `ForeignKey(unique=True)` |
| `created_at` | `DateTimeField` | `auto_now_add=True` | Unchanged |

### Indexes

| Index | Fields | Notes |
|-------|--------|-------|
| `payment_idx` | `payment` | Unchanged |
| `reservation_idx` | `reservation` | Unchanged (regular index; implicit unique index also exists from `OneToOneField`) |

### Relationships

```
Payment (1) ──< (N) PaymentReservation (1) ── (1) Reservation
```

- **Payment → PaymentReservation**: One-to-many via `payment_reservations` related name
- **Reservation → PaymentReservation**: One-to-one via `payment_links` related name

### Migration Impact

The migration will be an `AlterField` operation. At the database level, the schema is unchanged (`ForeignKey(unique=True)` and `OneToOneField` produce identical DDL), so:

- **Forward migration**: No SQL changes; state-only operation
- **Reverse migration**: Safe rollback to `ForeignKey(unique=True)`
- **Data**: No data migration needed; existing records are preserved

### Validation Rules

- A `Reservation` can have zero or one `PaymentReservation` (enforced by unique constraint)
- Cascade delete: deleting a `Reservation` deletes its `PaymentReservation`
- Cascade delete: deleting a `Payment` deletes all its `PaymentReservation` records

### Related Entities (Unchanged)

- **Payment**: Core payment record with client, amount, type, date, etc.
- **Reservation**: Equipment/climbing reservation record with client, date, status, etc.
