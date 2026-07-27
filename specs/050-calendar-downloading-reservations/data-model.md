# Data Model: Calendar Downloading in Reservations Page

## Entities

### Reservation

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| client | FK -> Client | The client who booked |
| class_slot | FK -> ClassSlot | The class slot reserved |
| date | date | Date of the reservation |
| equipment | FK -> Equipment (nullable) | Equipment reserved |
| payment | FK -> Payment (nullable) | Associated payment, null if unassociated |
| status | str | Reservation status (confirmed/cancelled/etc.) |
| created_at | datetime | Timestamp of creation |
| updated_at | datetime | Timestamp of last update |

### Payment

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| identifier | str | Human-readable payment identifier (shown to user) |
| client | FK -> Client | Client who paid |
| amount | decimal | Payment amount |
| date | date | Payment date |
| ... | ... | Other payment fields |

### ICS Calendar File (generated artifact)

Not a persisted entity. Generated on-demand as a response to a download request.

| Property | Description |
|----------|-------------|
| Version | 2.0 |
| Timezone | America/Denver |
| Events | One per Reservation in the date range |
| Filename | `<start_date>_<end_date>.ics` |

## Relationships

```
Reservation N:1 ──── Client
Reservation N:1 ──── ClassSlot
Reservation N:1 ──── Equipment (optional)
Reservation N:1 ──── Payment (optional)
Payment     1:N ──── Reservation
```

## Validation Rules

- Date range is required (start_date and end_date)
- End date must be >= start date
- Reservations outside the date range are excluded
- Reservations with no payment show "Reservación sin asociar" as payment identifier
