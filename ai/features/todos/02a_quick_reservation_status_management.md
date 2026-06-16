# Quick Reservation Status Management

## Description

As an Operator, I want to quickly mark reservations as "used" or "unused" 
directly from the reservation list view, with bulk operations to mark 
multiple reservations at once.

1. **Inline row actions**: Each reservation row in the list shows small 
   buttons to mark as "used" or "unused" without navigating to the detail page.
2. **Status badges**: Reservation status is displayed as a colored badge 
   (green=reserved, blue=used, gray=unused) for at-a-glance identification.
3. **Bulk operations**: A checkbox column allows selecting multiple 
   reservations and marking them as "used" or "unused" with a single click.
4. **Select All**: A header checkbox toggles all visible reservations.
5. **HTMX-powered**: Status changes update the row in-place without page 
   reload, providing instant feedback.

## Technical Notes

- Reuse the existing `reservation_change_status` view for single-row actions
- New `reservation_bulk_status` view for bulk operations (POST, accepts 
  `reservation_ids[]` array + `status` string)
- Templates to modify: `reservation_list.html`, `reservation_list_by_slot.html`
- Each `<tr>` wrapped with a unique `id="row-{{ r.pk }}"` for HTMX targeting
- Bulk toolbar appears/hides with CSS when checkboxes are checked (simple JS)
- Update `test_reservations_list.py` with bulk operation tests