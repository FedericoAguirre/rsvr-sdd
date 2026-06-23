# Quickstart: Quick Reservation Status Management

## What this feature does

Operators can mark reservations as "used" or "unused" directly from the reservation list view by clicking inline buttons. Each reservation row shows a colored status badge. Status changes happen instantly without page reload via HTMX.

## Files to modify

| File | Action |
|------|--------|
| `backend/apps/reservations/views.py` | Modify `reservation_change_status` to return HTMX partial |
| `backend/apps/reservations/templates/reservations/reservation_list.html` | Add status badges + inline action buttons |
| `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html` | Add status badges + inline action buttons |

## Files to create

| File | Purpose |
|------|---------|
| `backend/apps/reservations/templates/reservations/partials/reservation_row.html` | Partial template for HTMX row swap |
| `backend/apps/reservations/templatetags/reservation_extras.py` | Template filter for status badge CSS class |

## Tests to add

In `backend/tests/test_reservations_list.py`:

- **HTMX request returns row partial**: POST with `HTTP_HX_REQUEST="true"` → status 200, HTML contains `<tr` with updated badge
- **Non-HTMX request still redirects**: POST without HX header → redirect to detail page (existing behavior preserved)
- **Invalid status via HTMX**: POST with invalid status + HX header → 400 response
- **Unauthenticated HTMX request**: POST without login + HX header → redirect to login
- **Status badge rendering**: Verify correct badge class per status value in list view

## Implementation order

1. Create `reservation_extras.py` template tag (status badge CSS class mapping)
2. Create `partials/reservation_row.html` partial template
3. Modify `reservation_change_status` view for HTMX support
4. Update `reservation_list.html` with badges and inline buttons
5. Update `reservation_list_by_slot.html` with badges and inline buttons
6. Write and run tests
7. Run Ruff linter

## Dependencies

No new Python packages required. HTMX 2.0 is already loaded from CDN in `base.html`.
