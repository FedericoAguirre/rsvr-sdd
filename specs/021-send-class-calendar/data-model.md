# Data Model: Send Class Reservations Calendar to Client

## Overview

No new entities or database tables are introduced. This feature uses four existing entities to generate ICS calendar events.

## Entity Usage

### Reservation

| Field | Type | Used For |
|-------|------|----------|
| `id` | AutoField | Identifying which reservations to include |
| `client` | ForeignKey (Client) | Filtering by client, including client name in event |
| `class_slot` | ForeignKey (ClassSlot) | Getting slot name and time for event |
| `equipment` | ForeignKey (Equipment) | Including equipment name in event description |
| `date` | DateField | Event date, filename date formatting |
| `status` | CharField | Implicit — all statuses are included |
| `created_by` | ForeignKey (User) | Not used |
| `updated_by` | ForeignKey (User) | Not used |
| `notes` | TextField | Not used |
| `created_at` | DateTimeField | Not used |
| `updated_at` | DateTimeField | Not used |

**Query**: `client.reservations.select_related("equipment", "class_slot").filter(date__gte=start, date__lte=end)`

### Client

| Field | Type | Used For |
|-------|------|----------|
| `id` | AutoField | URL parameter, query filter |
| `first_name` | CharField | Event description, filename generation |
| `last_name` | CharField | Event description, filename generation |

**Filename**: `client_name` = `first_name` + ` ` + `last_name` → snake_case (lowercase, spaces→underscores, remove non-alphanumeric).

### ClassSlot

| Field | Type | Used For |
|-------|------|----------|
| `id` | AutoField | Joining via Reservation |
| `day_of_week` | IntegerField | Not directly used |
| `time` | TimeField | Event start time (combined with reservation.date) |
| `is_active` | BooleanField | Not used for filtering |

**Event title**: Formatted from `str(class_slot)` e.g., "Monday 17:30".

### Equipment

| Field | Type | Used For |
|-------|------|----------|
| `id` | AutoField | Joining via Reservation |
| `name` | CharField | Included in event description |

## Validation Rules

- **Date range**: Start date must not be after end date (validated before querying).
- **Empty result**: If no reservations match the date range, return a user-facing message, not a file.

## State Transitions

None — this is a read-only export feature. No data is modified.
