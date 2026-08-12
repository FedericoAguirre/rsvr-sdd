# Data Model: Batch Payment-Day Reservations

## Existing Entities

### Payment

- **Identity**: Primary key.
- **Relevant fields**: `date`, `created_at`, `client`, and `class_slot_count`.
- **Role**: Supplies the payment date, same-day payment timestamp, client reservation history, and required reservation count.
- **Lifecycle**: Created before the batch modal opens; may later have zero, partial, or complete payment-reservation associations.

### ClassSlot

- **Identity**: Primary key; unique by `day_of_week` and `time`.
- **Relevant fields**: `day_of_week`, `time`, and `is_active`.
- **Role**: Defines recurring active class availability and the start time used for same-day eligibility.

### Reservation

- **Identity**: Primary key; unique by `equipment`, `class_slot`, and `date`.
- **Relevant fields**: `client`, `equipment`, `class_slot`, `date`, and `status`.
- **Role**: Existing reservations shift the candidate start date and prevent conflicting new reservations.

### PaymentReservation

- **Identity**: Primary key; one-to-one with a reservation.
- **Relevant fields**: `payment` and `reservation`.
- **Role**: Associates each created batch reservation with the payment.

## Derived Reservation Window

The shared window calculation derives:

- **Candidate start**: the later of `Payment.date` and one day after the client's latest reservation date.
- **Same-day cutoff**: the local time from `Payment.created_at` when its local date equals `Payment.date`.
- **First eligible date**: candidate start when it has an active class slot after the cutoff; otherwise the next calendar date with an active class slot.
- **End date**: first eligible date plus 20 calendar days.

## Validation Rules

- Requested dates must parse as ISO calendar dates.
- The number of unique dates must equal `Payment.class_slot_count` and must not exceed 20.
- Every selected date must fall within the derived window.
- The selected class time must have an active class slot on each selected date's weekday.
- Equipment must remain in service and the selected class slot must remain active at submission time.
- Existing reservation uniqueness and partial-failure behavior remain unchanged.
