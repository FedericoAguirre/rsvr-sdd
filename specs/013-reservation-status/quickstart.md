# Quickstart: Add Reservation Status

## Prerequisites

- Docker and Docker Compose installed
- Python 3.13 (if running locally without Docker)

## Key Decisions

1. **Status field**: Django `CharField` with `choices` (following `Equipment.status` pattern)
2. **Status values**: `reserved` (default), `used`, `unused`
3. **Status change**: Via dedicated POST endpoint on reservation detail (not via edit form)
4. **i18n**: Use existing Django i18n + Spanish locale
5. **TDD**: Tests first, then implementation

## Files to Create

| File | Action | Purpose |
|------|--------|---------|
| `backend/apps/reservations/migrations/0003_reservation_status.py` | New | Add status field to Reservation model |
| `backend/apps/reservations/templates/reservations/reservation_detail.html` | Modify | Add status display + change buttons |
| `backend/apps/reservations/templates/reservations/reservation_list.html` | Modify | Add status column to table |
| `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html` | Modify | Add status column to table |
| `backend/apps/reservations/templates/reservations/reservation_list_pdf.html` | Modify | Add status column to PDF table |

## Files to Modify

| File | Changes |
|------|---------|
| `backend/apps/reservations/models.py` | Add `status` CharField with choices (default: "reserved") |
| `backend/apps/reservations/views.py` | Add `reservation_change_status` view; update detail view context |
| `backend/apps/reservations/urls.py` | Add path for status change endpoint |
| `backend/apps/reservations/admin.py` | Add `status` to list_display |
| `backend/locale/es/LC_MESSAGES/django.po` | Add translations for "Reserved", "Used", "Unused" |
| `backend/tests/test_reservations_list.py` | Add test classes for status display, filtering, and changes |

## Commands

```bash
# Run tests
docker-compose exec web python -m pytest

# Create migration after model change
docker-compose exec web python manage.py makemigrations reservations

# Apply migrations
docker-compose exec web python manage.py migrate

# Compile translations (after updating django.po)
docker-compose exec web python manage.py compilemessages
```

## Test Run Command

```bash
docker-compose exec web python -m pytest -v
```

To run only reservation tests:
```bash
docker-compose exec web python -m pytest backend/tests/test_reservations_list.py -v
```
