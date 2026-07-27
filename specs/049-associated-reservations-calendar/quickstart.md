# Quickstart: Associated Reservations Calendar Download

## Run the feature

```bash
docker compose up -d --build
```

## Endpoints

| URL | Purpose |
|-----|---------|
| `/payments/<id>/` | Payment detail page with "Descargar calendario" button |
| `/payments/<id>/calendar/` | Download ICS calendar for associated reservations |

## Test

```bash
# Run all tests
docker compose exec web pytest

# Run payment calendar-specific tests
docker compose exec web pytest tests/test_payments_calendar.py -v
```

## Manual test flow

1. Go to `/payments/<id>/` for a payment that has associated reservations
2. Click the "Descargar calendario" button
3. An ICS file downloads with the correct filename format
4. Open the ICS file in a calendar app — each reservation appears as an event with client name, class slot, date, equipment, and payment identifier
5. Repeat for a payment with zero reservations — a message is shown instead of a file download

## Key constraints

- No new models or database changes (FR-002 uses existing PaymentReservation association)
- ICS generation uses `icalendar` library (existing dependency)
- Timezone is America/Denver (consistent with feature 021)
- Filename uses snake_case client name + payment identifier + date range (FR-005)
