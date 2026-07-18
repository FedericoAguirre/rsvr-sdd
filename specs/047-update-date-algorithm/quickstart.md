# Quickstart: Update Auto-Date Algorithm

## Implementation Steps

1. **Update JS algorithm** (`backend/apps/reservations/static/reservations/js/auto-date.js`):
   - Lines 27-33: Change the `daysAhead` calculation to always produce a date in the next week
   - New formula: `daysAhead = (slotDay - todayDay + 14) % 7 + 7`

2. **Update Python algorithm** (`backend/apps/reservations/views.py`):
   - Lines 185-191: Mirror the same logic change in `auto_date_for_slot()`

3. **Update tests** (`backend/tests/test_reservations.py`):
   - `test_future_day_this_week`: Change expected assertion — future day now resolves to next week (diff + 7)
   - Verify all tests still pass

## Test Commands

```bash
# Run auto-date tests only
docker compose exec web uv run manage.py test backend.tests.test_reservations.TestAutoDate --verbosity=2

# Full suite
docker compose exec web uv run manage.py test --verbosity=2
```

## Key Files

| File | Change |
|------|--------|
| `backend/apps/reservations/static/reservations/js/auto-date.js` | Algorithm in `autoDate()` function |
| `backend/apps/reservations/views.py` | Algorithm in `auto_date_for_slot()` |
| `backend/tests/test_reservations.py` | Update `test_future_day_this_week` assertion |
