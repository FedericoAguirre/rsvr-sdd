# Quickstart: Batch Payment-Day Reservations

## Prerequisites

- Run commands from the repository root.
- Install the project's development dependencies with `uv sync`.
- Ensure the test database is available through the repository's normal pytest setup.

## Automated validation

Baseline before implementation: the existing batch test module passed 11 tests when run from `backend/`.

Run the focused batch-reservation tests:

```bash
uv run pytest backend/tests/test_payments_batch.py
```

Run the full test suite before implementation is considered complete:

```bash
uv run pytest
```

## Required boundary scenarios

Use a payment dated August 11, 2026 with five classes and active Tuesday/Wednesday slots at 19:15 and 20:15. Verify the `batch-data` response and modal date grid for:

1. 17:00: payment-day 19:15 and 20:15 remain eligible; range ends August 31.
2. 19:00: payment-day 19:15 and 20:15 remain eligible; range ends August 31.
3. 19:20: 19:15 is excluded and 20:15 remains eligible; range ends August 31.
4. 20:20: Tuesday slots are excluded; range begins August 12 and ends September 1.

For each scenario, submit exactly five dates and verify that reservations are associated with the payment. Also verify that existing maximum-count, weekday, capacity, conflict, and partial-failure tests continue to pass.

## Manual browser check

Open a newly created payment with a positive class count and confirm that the batch modal displays the returned date range, allows the required number of dates to be selected, and redirects to payment detail after successful creation. Confirm that invalid or conflicting submissions show the existing actionable error behavior.
