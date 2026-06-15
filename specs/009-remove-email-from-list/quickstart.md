# Quickstart: Remove Email from Client Column

**Feature**: [spec.md](./spec.md)

## Prerequisites

- Running Docker Compose stack (`make up`)
- Tests pass: `docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings -T web python -m pytest`

## Implementation Order

1. Add `full_name` template filter in `backend/apps/reservations/templatetags/reservation_extras.py`
2. Modify 3 templates: `reservation_list.html`, `reservation_list_by_slot.html`, `reservation_list_pdf.html` — replace `{{ r.client }}` with `{{ r.client|full_name }}`
3. Add tests verifying no email appears in any of the 3 list views
4. Run full test suite: `docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings -T web python -m pytest`

## Key Files

| File | Purpose |
|------|---------|
| `backend/apps/reservations/templatetags/reservation_extras.py` | New — `full_name` filter |
| `backend/apps/reservations/templates/reservations/reservation_list.html` | Modify 2 occurrences of `{{ r.client }}` |
| `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html` | Modify 1 occurrence |
| `backend/apps/reservations/templates/reservations/reservation_list_pdf.html` | Modify 1 occurrence |
| `backend/tests/test_reservations_list.py` | Add new test class/assertions |
