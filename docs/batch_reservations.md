# Batch Reservations After Payment

When an operator creates a payment with class slots, the batch reservation modal includes classes that have not started yet on the payment date.

## Date Window

- If a class remains later on the payment date, the window starts on that date.
- If all payment-day classes have started, the window starts on the next date with an active class slot.
- The window ends 20 calendar days after its first eligible date.
- Existing client reservation, class count, capacity, availability, weekday, and conflict rules continue to apply.
- Dates in the batch modal remain under their actual weekday columns, including when the window starts midweek; leading weekday cells are left empty rather than shifting dates left.

## Example

For August 11, 2026:

- At 17:00 or 19:00, Tuesday classes at 19:15 and 20:15 remain available and the window ends August 31.
- At 19:20, the 19:15 class is no longer available, while the 20:15 class remains available.
- At 20:20, the window starts Wednesday, August 12, and ends September 1.

The operator must select exactly the number of classes included in the payment before submitting the batch reservation.
