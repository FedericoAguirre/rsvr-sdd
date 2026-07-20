# Quickstart: Batch Reservations from Payment

## Run the feature

```bash
docker compose up -d --build
```

## Endpoints

| URL | Purpose |
|-----|---------|
| `/payments/create/` | Create a payment → triggers batch modal on success |
| `/payments/<id>/` | Payment detail page showing associated reservations |

## Test

```bash
# Run all tests
docker compose exec web pytest

# Run batch-specific tests
docker compose exec web pytest tests/test_payments_batch.py -v
```

## Manual test flow

1. Go to `/payments/create/` and fill in the form
2. Submit the payment
3. The batch modal appears automatically
4. Select equipment, class slot, and N dates (N = block class count)
5. Submit → N reservations created and linked to payment
6. Close modal → redirected to payment detail showing all linked reservations

## Key constraints

- Max 20 reservations per batch (FR-007)
- Dates limited to next Monday + 28 days (FR-003)
- Must select exactly N dates = block class count (FR-009)
- Only DOW-matching dates shown based on selected class slot (FR-014)
- Partial failure on unique constraint conflicts (no full rollback)
