# Data Model: Restore 20-Day Batch Reservation Window

## BatchReservationWindow

An in-memory value representing the date interval available for batch selection.

Fields:

- `start`: first eligible calendar date selected by the existing payment-day and reservation rules.
- `end`: inclusive calendar date reached after counting 20 selectable Monday-through-Friday dates from `start`.
- `same_day_cutoff`: payment-day time cutoff used only when validating the payment date.
- `target_weekday_count`: fixed business target of 20 selectable weekdays; represented by the calculation rather than a persisted field.

Rules:

1. The existing start-date algorithm remains authoritative.
2. If `start.weekday() < 5`, it counts as the first selectable weekday; otherwise counting begins at the next weekday while preserving the existing start value.
3. Each Monday-through-Friday date increments the count; Saturday and Sunday do not.
4. The loop stops when the count reaches 20, and that date becomes the inclusive `end`.
5. No payment, reservation, or class-slot schema changes are required.

## Related Entities

### Payment

Supplies the payment date, creation timestamp, client, and purchased class count.

### Reservation

Existing client reservations constrain the start date and are returned as reserved dates to the modal.

### ClassSlot

Active weekday/time records determine whether a candidate start date has an eligible class and whether selected dates can be validated.

## Derived UI Data

The existing `date_range` response is expanded semantically, not structurally: the browser iterates from `start` through the new `end`, skips weekends, omits reserved dates, and places remaining dates in their existing weekday columns.
