# Quickstart: Price Format Display

**Feature**: 063-price-format
**Date**: 2026-08-02

## Prerequisites

- PostgreSQL running (`make db-up`)
- Django environment active (`uv run manage.py` accessible)
- At least one `ClassPrice` record in the database

## Setup

No setup required — this is a template-only change. No migrations, no dependencies.

After applying the template change, restart the development server:

```bash
# If running via Docker
make docker-build && make docker-up

# If running locally
uv run manage.py runserver
```

## Validation Scenarios

### VS-001: Current prices display formatted

1. Navigate to `/classes/prices/` (the class prices page)
2. In the "Current prices" alert, verify price is displayed as `$N,NNN.NN` (e.g., `$100.00`, `$1,500.00`)
3. **Expected**: Every price has a `$` prefix, comma thousand separators, and exactly 2 decimal places

### VS-002: Price history table displays formatted

1. Scroll to the price history table on the same page
2. Verify each price in the "Price" column is formatted as `$N,NNN.NN`
3. **Expected**: Same format as current prices — consistent across the page

### VS-003: Enter new price and verify formatting

1. Click "Add new price" button
2. Enter a price like `1500` in the numeric input
3. Submit the form
4. After redirect back to the price list, verify the new price displays as `$1,500.00`
5. **Expected**: New price appears formatted; form entry workflow is unbroken

### VS-004: Null/edge cases

1. If no prices exist, the page loads without errors
2. If a price of `0.00` exists, it displays as `$0.00` (not an empty string or error)
3. **Expected**: Graceful handling — no template errors or 500 responses

## Running Tests

```bash
# Run class-related tests
uv run manage.py test apps.classes

# Run full suite
uv run manage.py test
```

**Expected**: All existing tests pass. New template rendering tests pass (asserting formatted output in rendered HTML).
