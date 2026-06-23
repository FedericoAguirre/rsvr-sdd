# Research: Send Class Reservations Calendar to Client

## ICS Generation Library

- **Decision**: Use `icalendar>=5.0`
- **Rationale**: `icalendar` is the most widely used Python library for generating RFC 5545 compliant iCalendar files. It supports VEVENT, timezone definitions, and standard calendar properties. It is well-maintained and compatible with Django.
- **Alternatives considered**: `ics` library (less mature, smaller ecosystem), manual string construction (error-prone, non-compliant).

## Event Time Handling

- **Decision**: Each calendar event uses `reservation.date` combined with `class_slot.time` as the event start time. End time is start + 1 hour (standard class duration).
- **Rationale**: ClassSlot model stores a `time` field (TimeField) with typical values 17:30 or 18:30. Reservation stores the `date` (DateField). Combining these gives precise event times.
- **Alternatives considered**: All-day events (loses precision, no time information in calendar), fixed duration.

## Timezone Handling

- **Decision**: All event timestamps use `America/Denver` timezone (VTIMEZONE component included in ICS).
- **Rationale**: The project's `TIME_ZONE` setting is `America/Denver`. ICS files with explicit timezone definitions ensure correct display across different calendar applications.
- **Alternatives considered**: Floating time (no timezone — ambiguous for recipients in different time zones), UTC-only.

## Filename Generation (snake_case)

- **Decision**: Generate snake_case client name by lowercasing, replacing spaces with underscores, and removing non-alphanumeric characters (except underscores).
- **Rationale**: Simple, predictable transformation that produces valid filenames.
- **Alternatives considered**: Django's `slugify()` (too aggressive, removes underscores), manual mapping of accented characters.

## Download Approach

- **Decision**: Django view returns an `HttpResponse` with `Content-Type: text/calendar` and `Content-Disposition: attachment` header.
- **Rationale**: Standard Django pattern for file downloads (already used in `client_csv_template` view). Lightweight, no additional dependencies needed.
- **Alternatives considered**: Streaming response (unnecessary for <100 events), temporary file on disk (extra cleanup needed).

## Date Range Input

- **Decision**: Two HTML `<input type="date">` fields for start and end dates on the client detail page. Form submitted via GET to the calendar endpoint.
- **Rationale**: Native browser date pickers, no JavaScript needed. GET request makes the URL bookmarkable and cacheable.
- **Alternatives considered**: JavaScript date range picker (heavier, adds JS dependency), POST request (non-bookmarkable).

## Client Name in Event Details

- **Decision**: Event TITLE/SUMMARY = "Class: {class_slot_name}". Event DESCRIPTION includes client name, class slot name, date, and equipment.
- **Rationale**: Following standard calendar event conventions where SUMMARY is a short title and DESCRIPTION contains full details.
- **Alternatives considered**: Putting everything in SUMMARY (too verbose for calendar views).
