# Data Model: Payments Columns Stripe

## Overview

No new entities, fields, or relationships are introduced by this feature. The existing data model for payments and reservations remains unchanged.

## Entities (Existing, referenced by the template)

### Payment

Represents a financial transaction (payment) made by a client. Each payment can have zero or more associated reservations.

**Key fields used in the grid context**:
- `id` — primary key (used in URL: `payments/{id}/`)
- `client` — ForeignKey to Client
- `amount`, `payment_type`, `date` — displayed in the detail card

### ReservationPayment (join table)

Links a `Reservation` to a `Payment`. The template iterates over `payment.reservationpayment_set.all` (passed as `reservations` in context).

**Fields**:
- `payment` — ForeignKey to Payment
- `reservation` — ForeignKey to Reservation

### Reservation

A booking for a specific class slot on a specific date.

**Fields displayed in the grid**:
- `date` — date of the reservation
- `class_slot` — ForeignKey to ClassSlot (displayed as its string representation)
- `equipment` — the equipment used (e.g., Treadmill, Climbing gear)
- `status` — CharField with choices (`get_status_display()`) for display

## Relationships

```
Payment 1──* ReservationPayment *──1 Reservation
```

## Validation

No validation changes. The template is read-only display only.
