# Research: Calendar Downloading in Reservations Page

## Overview

Research conducted to inform the implementation of calendar (ICS) download functionality in the reservations page, including payment identifier in event descriptions.

## Existing ICS Generation Patterns

### Clients App (`backend/apps/clients/views.py`)

- Contains `_generate_ics(client, reservations, start_date, end_date)` — a module-level function
- Builds ICS with:
  - Timezone: America/Denver
  - 1-hour events per reservation
  - Summary: class slot name
  - Description: Client, Class, Date, Equipment
- Called by `client_calendar` view (GET with start_date/end_date query params)
- URL: `clients/<int:pk>/calendar/`

### Payments App (`backend/apps/payments/views.py`)

- Contains duplicated inline ICS generation in `payment_calendar` view
- Nearly identical to clients' `_generate_ics` but with:
  - Different `prodid` value
  - Extra `\nPago:` line in DESCRIPTION
- URL: `payments/<int:pk>/calendar/`

## Decision: Extract Shared Utility

**Decision**: Create `backend/utils/ical.py` with a refactored `generate_ics(reservations, prodid, extra_description_lines=None)` function.

**Rationale**:
- Eliminates code duplication (identical timezone setup, event creation loop)
- Single point of maintenance for ICS format changes
- All three apps (clients, payments, reservations) can import and use it
- Backward compatible — existing views keep same behavior

**Alternatives considered**:
- Keep duplicated code — rejected because it violates Code Quality (Principle I)
- Put utility in `clients/views.py` and import from other apps — rejected because utils should live in a neutral location

## Technical Details

### icalendar Library

- Package: `icalendar` (already in project dependencies)
- Classes: `Calendar`, `Event`, `Timezone`, `TimezoneStandard`, `TimezoneDaylight`
- Timezone setup: literal `America/Denver` with hardcoded offset values (existing pattern)

### Shared Utility Contract

```python
def generate_ics(reservations, prodid, extra_fields_fn=None):
    """
    Generate ICS calendar content for a list of reservations.
    
    Args:
        reservations: QuerySet of Reservation objects
        prodid: str, product identifier for the calendar
        extra_fields_fn: Optional callable(reservation) -> dict
            that returns extra fields to add to the event description
    
    Returns:
        bytes: ICS file content
    """
```

### Filename Convention

- Clients: `<client_name_snake_case>_<start_date>_<end_date>.ics`
- Payments: `<client_snake_case>_<payment_identifier>_<first_date>_<last_date>.ics`
- Reservations: `<start_date>_<end_date>.ics` (or include filter description)

### i18n Strings Needed

- "Download Calendar" → "Descargar calendario"
- "Start date" → "Fecha de inicio"
- "End date" → "Fecha de fin"
- "No reservations found in the selected date range." → "No se encontraron reservaciones en el rango de fechas seleccionado."
