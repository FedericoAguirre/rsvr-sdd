# Data Model: List Unassociated Reservations on Payments Page

## Entities

### Reservation (existing, unmodified)

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| client | FK -> Client | The client who booked |
| equipment | FK -> Equipment | Equipment reserved |
| class_slot | FK -> ClassSlot | The class slot reserved |
| date | date | Date of the reservation |
| status | str | Reservation status (reserved/used/unused) |
| notes | text | Optional notes |
| created_by | FK -> User | Who created the reservation |
| updated_by | FK -> User (nullable) | Who last updated |
| created_at | datetime | Timestamp of creation |
| updated_at | datetime | Timestamp of last update |

### PaymentReservation (existing, unmodified)

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| payment | FK -> Payment | Associated payment |
| reservation | FK -> Reservation (unique) | Associated reservation (one-to-one from reservation side) |
| created_at | datetime | Timestamp of creation |

### Client (existing, unmodified)

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| first_name | str | First name |
| last_name | str | Last name |
| ... | ... | Other client fields |

## Relationships

```
Reservation     N:1 ──── Client
Reservation    0..1 ──── PaymentReservation (via payment_links, unique)
PaymentReservation 1:1 ──── Reservation (unique=True)
PaymentReservation N:1 ──── Payment
Client         1:N ──── Reservation
Client         1:N ──── Payment
```

## Query Concept: Unassociated Reservation

Not a new entity. An "unassociated reservation" is a Reservation filtered by:
- `client_id = {target client}`
- No `PaymentReservation` link exists (i.e., `payment_links = None`)

## Validation Rules

- `client_id` is required and must reference an existing Client
- A reservation with an existing PaymentReservation link MUST NOT appear in the list
- Reservations must be returned ordered by `-date, class_slot__time` (most recent first)
