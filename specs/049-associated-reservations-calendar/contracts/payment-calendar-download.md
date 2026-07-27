# Contract: Payment Calendar Download

## Endpoint

```
GET /payments/{pk}/calendar/
```

## Response (Success — Reservations Exist)

- **Status**: `200 OK`
- **Content-Type**: `text/calendar; charset=utf-8`
- **Content-Disposition**: `attachment; filename="<client_snake_case>_<payment_identifier>_<first_date_YYYYMMDD>_<last_date_YYYYMMDD>.ics"`
- **Body**: Valid ICS (iCalendar) file conforming to RFC 5545

### ICS Structure

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//rsvr-sdd//Payment Reservations//EN
BEGIN:VTIMEZONE
TZID:America/Denver
...
END:VTIMEZONE
BEGIN:VEVENT
DTSTART;TZID=America/Denver:20260721T191500
DTEND;TZID=America/Denver:20260721T201500
SUMMARY:Lunes 19:15 (Eliptico 2)
DESCRIPTION:Cliente: Jane Doe\nClase: Lunes 19:15\nFecha: 2026-07-21\nEquipo: Eliptico 2\nPago: EF20260721001
END:VEVENT
...
END:VCALENDAR
```

### Event Fields

| ICS Field | Source | Notes |
|-----------|--------|-------|
| `DTSTART` | `reservation.date` + `class_slot.time` | Timezone-aware (America/Denver) |
| `DTEND` | `DTSTART` + 1 hour | Fixed 1-hour duration |
| `SUMMARY` | `class_slot.__str__()` or `class_slot.name` | Short title |
| `DESCRIPTION` | Client name, slot name, date, equipment, payment identifier | Includes "Pago:" field |

## Response (Empty — No Reservations)

- **Status**: `302 Redirect` (redirect back to payment detail page)
- **Flash message**: Message indicating no reservations are associated with this payment

## Authentication

- **Required**: User must be logged in (`LoginRequiredMixin`)
- **Authorization**: Any authenticated staff/operator can download calendar for any payment

## Error States

| Condition | Response |
|-----------|----------|
| Payment not found (`pk` invalid) | `404 Not Found` |
| Payment has no associated reservations | Redirect with informative message (no file generated) |
| User not authenticated | `302 Redirect` to login page |

## Filename Format

```
<client_snake_case>_<payment_identifier>_<first_date_YYYYMMDD>_<last_date_YYYYMMDD>.ics
```

- `client_snake_case`: Client name converted to snake_case (lowercase, spaces → underscores, accents simplified)
- `payment_identifier`: The payment's unique identifier string (e.g., `EF20260721001`)
- `first_date`: Earliest reservation date in the set, formatted as `YYYYMMDD`
- `last_date`: Latest reservation date in the set, formatted as `YYYYMMDD`
- If only one reservation, both dates are the same
