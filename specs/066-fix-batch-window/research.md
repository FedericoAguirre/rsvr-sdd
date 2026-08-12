# Research: Restore 20-Day Batch Reservation Window

## Decision: Count selectable weekdays inclusively

- **Decision**: Keep the calculated start date and advance the end date until 20 Monday-through-Friday dates, including the start date when it is a weekday.
- **Rationale**: The existing modal intentionally skips Saturday and Sunday. The deployed payment record demonstrated that a 20-calendar-day interval from August 31 through September 20 exposes only 15 weekday buttons. Counting the selectable weekday dates directly matches the requirement and works across month/year boundaries and midweek starts.
- **Alternatives considered**: Keep 20 calendar days; rejected because it reproduces the reported 15-date behavior. Add a fixed 28-day offset; rejected because it is less explicit and can be wrong for a non-weekday start or future schedule changes. Change the modal to display weekends; rejected because weekends are not valid class dates in the current product.

## Decision: Keep the existing start-date algorithm

- **Decision**: Change only the end-date calculation after the existing payment-day, latest-reservation, active-weekday, and cutoff logic selects `window.start`.
- **Rationale**: The reported issue is a length mismatch, not a start-date defect. Preserving the start algorithm reduces regression risk for payment-day and associated-reservation behavior.
- **Alternatives considered**: Recalculate the entire window in the modal; rejected because the server-side form validation must share the same authoritative interval.

## Decision: Preserve the interface contract

- **Decision**: Keep `date_range.start`, `date_range.end`, `reserved_dates`, `class_slots`, and the batch-create payload unchanged; only the value of `date_range.end` changes.
- **Rationale**: Both the modal and `BatchReservationForm` already consume the shared range. A semantic correction to the end value requires no endpoint shape change.
- **Alternatives considered**: Add a `weekday_count` response field; rejected because the existing client can render the correct range from start and end, and a new field would add unnecessary contract surface.

## Deployment evidence

- **Decision**: Use the local deployed application/database as a regression fixture for the reported identifier without mutating deployment data.
- **Evidence**: `CASH20260811AC003` was found with payment date `2026-08-11`, five associated reservations, and a current calculated window of `2026-08-31` through `2026-09-20`; that interval contains 15 weekdays.
