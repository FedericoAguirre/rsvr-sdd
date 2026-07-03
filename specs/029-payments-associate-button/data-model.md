# Data Model: Payments Associate Button

## Summary

This feature does not introduce any new entities, fields, or database changes. It only adds a button and a read-only association page.

## Existing Entities Referenced

### Payment

- **Source**: `backend/apps/payments/models.py`
- **Role in this feature**: The payment whose ID is used to construct the associate URL and to query its client's reservations.
- **Key fields used**: `pk`, `client` (ForeignKey), `class_slot_count`, `payment_reservations` (related name)

### PaymentReservation

- **Source**: `backend/apps/payments/models.py`
- **Role in this feature**: Tracks existing associations to determine remaining available slots.

### Reservation

- **Source**: `backend/apps/reservations/models.py`
- **Role in this feature**: Listed on the associate page for the user to select and link to the payment.

## No Schema Changes

No migrations required. The feature operates entirely within existing database structures.
