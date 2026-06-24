# Data Model: Payments Module

## Entities

### Payment

Represents a financial transaction made by a client.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | AutoField (PK) | | Primary key |
| `client` | ForeignKey(Client) | NOT NULL, on_delete=PROTECT | The client who made the payment |
| `amount` | DecimalField | max_digits=10, decimal_places=2, NOT NULL | Payment amount in currency |
| `payment_type` | CharField | max_length=20, choices=PAYMENT_TYPES | Cash, credit card, debit card, electronic transfer, payments app |
| `payment_identifier` | CharField | max_length=50, UNIQUE, NOT NULL | Auto-generated: type acronym + YYYYMMDD + client initials + 3-digit consecutive |
| `date` | DateField | NOT NULL | Date the payment was made |
| `class_slot_count` | PositiveSmallIntegerField | NOT NULL, min=1 | Number of class slots this payment covers |
| `reference` | CharField | max_length=255, NULL, blank=True | Optional external reference |
| `evidence` | ImageField | upload_to=payments/evidence/, NULL, blank=True | Optional evidence image |
| `notes` | TextField | NULL, blank=True | Optional notes |
| `is_deleted` | BooleanField | default=False | Soft-delete flag |
| `deleted_at` | DateTimeField | NULL, blank=True | When soft-deleted |
| `created_at` | DateTimeField | auto_now_add=True | Creation timestamp |
| `updated_at` | DateTimeField | auto_now=True | Last update timestamp |
| `created_by` | ForeignKey(User) | on_delete=PROTECT, related_name=+ | Operator who created the payment |
| `updated_by` | ForeignKey(User) | on_delete=PROTECT, related_name=+, NULL | Operator who last modified the payment |

**Validation Rules**:
- `payment_identifier` must be unique across all payments (including soft-deleted)
- `amount` must be positive (> 0)
- `class_slot_count` must be at least 1
- Only `reference`, `notes`, and `evidence` can be modified after creation
- Evidence images limited to 5MB, JPEG/PNG only

**State Transitions**:
```
Created → Active (default)
Active → Soft-Deleted (via delete action)
Soft-Deleted → (no undelete — permanent or DB restore)
```

### PaymentReservation (Junction Model)

Links a payment to the reservations it covers.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | AutoField (PK) | | Primary key |
| `payment` | ForeignKey(Payment) | NOT NULL, on_delete=CASCADE, related_name=reservations | The payment |
| `reservation` | ForeignKey(Reservation) | NOT NULL, on_delete=CASCADE, unique, related_name=payment_link | The reservation |
| `created_at` | DateTimeField | auto_now_add=True | When the association was made |

**Validation Rules**:
- A reservation can only be linked to one active (non-deleted) payment
- The count of linked reservations must not exceed the payment's `class_slot_count`
- The payment and reservation must belong to the same client

## Relationships

```
Client 1 ───< N Payment
Payment 1 ───< N PaymentReservation >─── 1 Reservation
Payment N ───> 1 PaymentType (via choices field)
Payment N ───> 1 User (created_by)
Payment N ───> 1 User (updated_by, nullable)
```

## Payment Identifier Format

```
{PREFIX}{YYYYMMDD}{INITIALS}{NNN}
```

- **PREFIX**: 2-3 letter acronym per type (e.g., CASH, CC, DC, TRANSF, PAPP)
- **YYYYMMDD**: Payment date (zero-padded)
- **INITIALS**: Client first initial + last initial, uppercase (e.g., "JD" for John Doe)
- **NNN**: 3-digit consecutive number, zero-padded, reset daily per payment type

**Example**: `CC20260624JD003` — third credit card payment on 2026-06-24 for John Doe

## Database Indexes

- `payment_identifier` (unique) — for lookup and uniqueness enforcement
- `(client, date DESC)` — for client payment history queries
- `(date, payment_type)` — for report aggregation queries
- `is_deleted` — for filtering soft-deleted records
- `PaymentReservation.(reservation)` (unique) — ensures one-to-one reservation-to-active-payment
