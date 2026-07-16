# Quickstart: Order Reservations by Date in Payment Detail

## Files to Change

1. **`backend/apps/payments/views.py`** — Line 130, add `.order_by()` to queryset
2. **`backend/tests/test_payments.py`** — Add ordering assertions

## Implementation

### View Change (`views.py:130`)

```python
# Before:
).all()

# After:
).order_by("-reservation__date", "-reservation__class_slot__time")
```

### Test Approach

Test requirements:
- Create 2+ reservations on different dates linked to the same payment
- Assert the response HTML shows most recent date first
- Create same-date reservations with different class slot times
- Assert latest time appears first

### Commands

```bash
# Run tests
docker compose exec web uv run pytest tests/test_payments.py -v

# Run linting
docker compose exec web uv run ruff check apps/payments/ tests/

# Run type checks
docker compose exec web uv run mypy apps/payments/
```

## Notes

- No migrations needed — schema is unchanged
- No i18n changes — no new strings
- Existing `select_related` chain is preserved
