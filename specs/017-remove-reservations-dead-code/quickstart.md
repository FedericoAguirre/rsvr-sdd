# Quickstart: Remove Reservations Dead Code

## What this feature does

Removes the redundant `/reservations/list/` endpoint, relocates Export PDF to `/reservations/pdf/`, and adds an `updated_by` field to the Reservation model.

## Steps

1. **Remove dead view and template**: Delete `reservation_list_by_slot` view from `views.py` and `reservation_list_by_slot.html` template.
2. **Relocate PDF export**: Rename URL from `list/pdf/` to `pdf/` in `urls.py`, update the view reference, and update the PDF URL in `reservation_list.html`.
3. **Create migration**: Run `python manage.py makemigrations reservations` to generate `0004_add_updated_by.py`. Delete the orphaned `.pyc` from `__pycache__/`.
4. **Remove dead tests**: Delete `TestClientColumnNoEmail` and `TestReservationsList` test classes from `test_reservations_list.py`.
5. **Verify**: Run `python manage.py migrate` and `pytest backend/tests/test_reservations_list.py -v`.
