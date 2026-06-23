# Quick Reservation Status Management

## Description

As an Operator, I want to quickly mark reservations as "used" or "unused" 
directly from the reservation list view, row by row.

1. **Inline row actions**: Each reservation row in the list shows small 
   buttons to mark as "used" or "unused" without navigating to the detail page.
2. **Status badges**: Reservation status is displayed as a colored badge 
   (green=reserved, blue=used, gray=unused) for at-a-glance identification.
3. **HTMX-powered**: Status changes update the row in-place without page 
   reload, providing instant feedback.

## Technical Notes

- Reuse the existing `reservation_change_status` view for single-row actions
- Templates to modify: `reservation_list.html`, `reservation_list_by_slot.html`
- Each `<tr>` wrapped with a unique `id="row-{{ r.pk }}"` for HTMX targeting
- Update `test_reservations_list.py` with row by row operation tests