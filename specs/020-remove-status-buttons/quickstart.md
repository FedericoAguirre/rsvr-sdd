# Quickstart: Remove Status Buttons from Reservation List

**Phase**: 1 (Design & Contracts)
**Date**: 2026-06-22

## What to change

Edit three template files:

1. `backend/apps/reservations/templates/reservations/reservation_list.html`
   - Remove the `<button>` elements with `hx-post` for "Used" and "Unused" status
   - Keep status badge (`{{ r.status|status_badge_class }}` / `{{ r.status|status_label }}`)

2. `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`
   - Same removal as above

3. `backend/apps/reservations/templates/reservations/partials/reservation_row.html`
   - Same removal as above

## What NOT to change

- `views.py` — the `reservation_change_status` view is still used by the detail page's forms
- `urls.py` — the `status/` route must remain for detail-page access
- `base.html` — the HTMX CSRF handler is unaffected
- `reservation_extras.py` — status badge filters are still used by badges

## Verify

```bash
cd backend && uv run python -m pytest tests/ --reuse-db -k "not PDF and not test_clear_filters_button_exists"
```
