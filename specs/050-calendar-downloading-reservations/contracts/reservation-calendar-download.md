# Contract: Reservation Calendar Download

## Endpoint

**URL**: `reservations/calendar/`
**Method**: GET
**Query Parameters**:
- `start_date` (required, format: YYYY-MM-DD)
- `end_date` (required, format: YYYY-MM-DD)

## Response

**Content-Type**: `text/calendar; charset=UTF-8`
**Content-Disposition**: `attachment; filename="<start_date>_<end_date>.ics"`

### Success (200)
Returns ICS file content with events for all reservations in the date range.

### Empty Range (200)
Returns ICS file with no events (empty calendar) or redirects with a message.

### Missing Parameters (400)
Returns error message if `start_date` or `end_date` is missing.

## ICS Format

- **Version**: 2.0
- **Timezone**: America/Denver
- **Filename**: `<start_date>_<end_date>.ics`
- **Each Event**:
  - DTSTART: reservation date + class slot time (America/Denver)
  - DTEND: DTSTART + 1 hour
  - SUMMARY: Class slot name
  - DESCRIPTION: Client name, Class, Date, Equipment, Payment identifier

## Event Description Format

```
Client: <client_name>
Class: <class_slot_name>
Date: <date>
Equipment: <equipment_name>
Payment: <payment_identifier>
```

If no payment is associated: `Payment: Reservación sin asociar`

## Shared Utility Contract

```python
def generate_ics(reservations, prodid="-//rsvr-sdd//Class Reservations//ES", extra_fields_fn=None):
    """
    Generate ICS calendar content for a list of reservations.
    
    Args:
        reservations: Iterable of Reservation objects with .client, .class_slot, .date, .equipment
        prodid: str, product identifier for PRODID field
        extra_fields_fn: Optional callable(reservation) -> dict
            Extra key-value pairs to include in description (e.g., {"Pago": payment_id})
    
    Returns:
        bytes: UTF-8 encoded ICS content
    """
```

## Filename Pattern

- Reservations: `<start_date>_<end_date>.ics`
- Clients: `<client_name_snake_case>_<start_date>_<end_date>.ics`
- Payments: `<client_name_snake_case>_<payment_id>_<first_date>_<last_date>.ics`
