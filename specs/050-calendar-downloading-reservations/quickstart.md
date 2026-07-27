# Quickstart: Calendar Downloading in Reservations Page

## Prerequisites

- Docker Compose running (`make up` or `docker compose up -d`)
- Django migrations applied (`docker compose exec web uv run manage.py migrate`)

## Implementation Steps

### 1. Create Shared ICS Utility

Create `backend/utils/ical.py`:

- Extract ICS generation from `clients/views.py::_generate_ics`
- Add `extra_fields_fn` parameter for customizable description fields
- Keep existing timezone setup (America/Denver)
- Keep existing event duration (1 hour)

### 2. Refactor Clients App

Update `clients/views.py`:
- Import `generate_ics` from `backend.utils.ical`
- Replace `_generate_ics` call with shared utility call
- Keep `client_calendar` view unchanged (same behavior)

### 3. Refactor Payments App

Update `payments/views.py`:
- Import `generate_ics` from `backend.utils.ical`
- Replace inline ICS generation with shared utility call
- Pass `extra_fields_fn` to add `Pago:` line to description

### 4. Add Reservations Calendar View

Create `reservations/views.py` calendar view:
- Accept `start_date` and `end_date` query parameters
- Filter reservations by date range
- Call `generate_ics` with reservations
- Add `extra_fields_fn` to include payment identifier
- Return ICS file response

### 5. Add URL Route

Add to `reservations/urls.py`:
```python
path("calendar/", views.reservation_calendar, name="reservation-calendar"),
```

### 6. Add UI Button

Add to `reservations/templates/reservations/reservation_list.html`:
- Date range input form (can reuse existing filter inputs)
- "Descargar calendario" submit button

### 7. i18n

- Extract new strings: `django-admin makemessages -l es`
- Translate strings in `backend/locale/es/LC_MESSAGES/django.po`
- Compile: `django-admin compilemessages`

### 8. Tests

Create `backend/tests/test_reservations_calendar.py`:
- Test ICS file generation
- Test payment identifier in description
- Test unassociated reservations
- Test empty date range
- Test filename format
- Test shared utility contract

## Verification

```bash
# Run calendar tests
docker compose exec web uv run pytest backend/tests/test_reservations_calendar.py -v

# Run shared utility tests
docker compose exec web uv run pytest backend/tests/test_ical_utils.py -v

# Full test suite
docker compose exec web uv run pytest

# Compile translations
docker compose exec web uv run manage.py compilemessages
```
