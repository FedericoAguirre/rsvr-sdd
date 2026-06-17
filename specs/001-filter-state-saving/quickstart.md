# Quickstart: Filter State Saving

**Plan**: [plan.md](plan.md)

## What This Feature Does

Preserves reservation filter values (class slot, date, status) across all postback operations on the reservations list page. When a user filters reservations and then paginates, sorts, edits, or performs any other action, the filter fields retain their selected values.

## Key Changes

- **`backend/apps/reservations/views.py`**: Ensure filter GET params are consistently passed to the template context
- **`backend/apps/reservations/templates/reservations/reservation_list.html`**: Add `selected` attribute to class_slot dropdown option matching the current filter value
- **`backend/tests/test_reservations_list.py`**: Add tests verifying filter state preservation in rendered HTML

## How to Test

```bash
docker-compose exec web python -m pytest tests/test_reservations_list.py -v
```

## Manual Verification

1. Navigate to `/reservations/`
2. Select a class slot, date, and status → click Filter
3. Verify all three filter fields show the selected values
4. Click "View" on a reservation → browser back → verify filters preserved
5. Navigate to a different page (e.g., Equipment) → back to Reservations → verify filters preserved (or reset on full reload — acceptable per spec)
