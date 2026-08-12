# Research: Batch Payment-Day Reservations

## Decision: Centralize the reservation-window calculation

**Rationale**: The current next-Monday/four-week calculation is duplicated in `BatchDataView` and `BatchReservationForm.clean_dates`. A shared helper ensures the modal display and server validation use identical start and end dates.

**Alternatives considered**:
- Change only the JSON view: rejected because invalid dates could still be submitted to the form.
- Change only form validation: rejected because the modal would hide valid payment-day dates.

## Decision: Use the payment creation timestamp for the same-day cutoff

**Rationale**: `Payment.date` stores only a calendar date, while `Payment.created_at` stores the timestamp created immediately after payment. Convert `created_at` to the configured `America/Denver` time zone and compare class start times against it when the payment date is the local creation date. This supports the 17:00, 19:00, 19:20, and 20:20 examples without adding a database field.

**Alternatives considered**:
- Use the current request time: rejected because it makes historical or delayed modal requests produce a different result.
- Add a payment-time field: rejected because the existing creation timestamp provides the required value and the feature does not require a schema change.

## Decision: Preserve the existing latest-reservation offset

**Rationale**: The current flow moves the candidate start date to the day after the client's latest reservation. This is an existing batch rule and must remain in force. The payment-day rule applies only when that offset does not move the candidate start beyond the payment date.

**Alternatives considered**:
- Always restart from the payment date: rejected because it could overlap an existing reservation for the same client.

## Decision: Advance to the next date with an active class slot

**Rationale**: When every class on the payment date has already started, the first eligible date is the next calendar date containing at least one active class slot. This matches the August 11 at 20:20 example and handles schedules without assuming every weekday has a class.

**Alternatives considered**:
- Always use the next calendar day: rejected because a schedule may have no class on that day.
- Keep the next-Monday rule: rejected because it conflicts with the requested immediate availability.

## Decision: Keep the existing endpoint shape

**Rationale**: The existing `batch-data` JSON response already exposes `date_range`, class slots, equipment, and reserved dates, and the existing modal consumes that shape. Only the values in `date_range.start` and `date_range.end` need to change.

**Alternatives considered**:
- Add a new endpoint or response version: rejected because no consumer needs a new contract.
