# Quickstart: Batch Reservation Date Alignment

## Prerequisites

- Repository checked out on `065-batch-reservation-date-alignment`.
- PostgreSQL available through the existing development setup.
- Python dependencies installed with `uv`.

## Focused Validation

From the repository root:

```bash
cd backend
uv run pytest tests/test_payment_detail_template.py -q
uv run pytest tests/test_payments_batch.py -q
```

Expected result: all existing batch reservation tests pass, including payment-day window, date validation, and reservation creation behavior.

## Browser Alignment Scenarios

1. Open a payment whose batch window begins on Tuesday, Wednesday, Thursday, or Friday.
2. Open the batch reservation modal.
3. Confirm the first date appears under its actual weekday header, with empty leading cells for earlier weekdays in that calendar week.
4. Confirm subsequent weeks begin under Monday and dates remain in their matching columns.
5. Select dates and submit the batch reservation.
6. Confirm the created reservations use the exact displayed dates and matching class weekdays.

## Full Validation

```bash
cd backend
uv run pytest
uv run ruff check apps/payments tests/test_payments_batch.py --select E,F,I
```

Expected result: the full test suite and targeted lint checks pass. Repository-wide documentation-only lint findings are tracked separately as existing baseline issues.

## Related Contracts

- [Batch reservation interface](contracts/batch-reservation.md)
- [Date-grid data model](data-model.md)
