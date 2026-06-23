# Contract: Client Calendar Download

## Endpoint

```
GET /clients/{pk}/calendar/
```

## Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | string (date) | Yes | Start of date range (inclusive), format `YYYY-MM-DD` |
| `end_date` | string (date) | Yes | End of date range (inclusive), format `YYYY-MM-DD` |

## Response (Success)

- **Status**: `200 OK`
- **Content-Type**: `text/calendar; charset=utf-8`
- **Content-Disposition**: `attachment; filename="cal_<client_snake_case>_<start_YYYYMMDD>_<end_YYYYMMDD>.ics"`
- **Body**: Valid ICS (iCalendar) file conforming to RFC 5545

### ICS Structure

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//rsvr-sdd//Class Reservations//EN
BEGIN:VTIMEZONE
TZID:America/Denver
...
END:VTIMEZONE
BEGIN:VEVENT
DTSTART;TZID=America/Denver:20260323T173000
DTEND;TZID=America/Denver:20260323T183000
SUMMARY:Monday 17:30
DESCRIPTION:Client: Jane Doe\nClass: Monday 17:30\nDate: 2026-03-23\nEquipment: Treadmill 1
END:VEVENT
...
END:VCALENDAR
```

### Event Fields

| ICS Field | Source | Notes |
|-----------|--------|-------|
| `DTSTART` | `reservation.date` + `class_slot.time` | Timezone-aware |
| `DTEND` | `DTSTART` + 1 hour | Fixed 1-hour duration |
| `SUMMARY` | `str(class_slot)` | Short title for calendar display |
| `DESCRIPTION` | Client name, slot name, date, equipment | Multi-line field |

## Response (Validation Error)

- **Status**: `400 Bad Request` (rendered as page with error message)
- **Body**: HTML page or message explaining the validation error (e.g., "Start date must be before end date")

## Response (Empty Result)

- **Status**: `200 OK`
- **Body**: HTML message indicating no reservations found in the given date range

## Authentication

- **Required**: User must be logged in (`@login_required` decorator)
- **Authorization**: Any authenticated staff/operator can access any client's calendar

## Error States

| Condition | Response |
|-----------|----------|
| Missing `start_date` or `end_date` | Error message displayed |
| `start_date > end_date` | Error message displayed |
| Invalid date format | Error message displayed |
| Client not found (`pk` invalid) | `404 Not Found` |
| User not authenticated | `302 Redirect` to login page |
