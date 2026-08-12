# Quickstart: Restore 20-Day Batch Reservation Window

## Prerequisites

- Branch `066-fix-batch-window` checked out.
- PostgreSQL available through the existing development setup.
- Python dependencies installed with `uv`.
- For deployment verification, the application and its database are running at the configured deployment URL.

## Focused Tests

From the repository root:

```bash
cd backend
uv run pytest tests/test_payments_batch.py -q
```

Expected result: window tests verify 20 weekday dates for Monday and midweek starts, the reported payment reaches September 25, 2026, and existing cutoff and latest-reservation tests retain their start dates.

## Reported Payment Verification

1. Locate payment `CASH20260811AC003` in the deployment without modifying its data.
2. Open its associated batch-reservation modal.
3. Count selectable weekday date buttons, excluding reserved dates according to existing behavior.
4. Confirm the calculated interval is long enough to contain 20 eligible weekdays; for the reported August 31 start with a Monday-Friday schedule, the end should reach September 25, 2026.
5. Select valid dates and confirm submitted reservations retain their exact calendar dates and class weekdays.

## Full Validation

```bash
cd backend
uv run pytest
uv run ruff check apps/payments/batch_reservations.py tests/test_payments_batch.py --select E,F,I
```

Expected result: all tests pass and changed Python files pass targeted lint.

## Related Contract

- [Batch reservation contract](contracts/batch-reservation.md)
- [Window data model](data-model.md)
