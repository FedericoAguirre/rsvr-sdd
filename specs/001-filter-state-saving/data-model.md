# Data Model: Filter State Saving

**Spec**: [spec.md](spec.md)

## Overview

No data model changes. This feature is a presentational bug fix — all entities remain unchanged.

## Existing Entities (Unchanged)

- **Reservation**: Equipment reservation with fields: `id`, `client` (FK), `equipment` (FK), `class_slot` (FK), `date`, `status` (reserved/used/unused), `notes`, `created_by` (FK), `created_at`, `updated_at`
- **ClassSlot**: Class time slots with fields: `id`, `day_of_week`, `time`, `is_active`
- **Client**: Gym members with fields: `id`, `first_name`, `last_name`, `email`, `mobile`, `is_active`
- **Equipment**: Equipment items with fields: `id`, `name`, `type`, `status`, `notes`

## Filter Form State (transient, not persisted)

| Field | Source | Type | Notes |
|-------|--------|------|-------|
| `class_slot` | `request.GET.get("class_slot")` | integer (PK) | Must be preserved across postbacks |
| `date` | `request.GET.get("date")` | string (YYYY-MM-DD) | Must be preserved across postbacks |
| `status` | `request.GET.get("status")` | string (reserved/used/unused) | Must be preserved across postbacks |

## State Transitions

Filter state is ephemeral — it exists only within the current page view lifecycle:
- **Apply**: User selects values and submits form → server processes GET params and re-renders with selected values
- **Postback**: Any server round-trip (sort, paginate, save, delete, etc.) → server re-populates filter fields from current request params
- **Clear**: User clicks "Clear Filters" → all params reset to default
- **Page refresh**: Browser full reload → all params reset to default (acceptable per spec)
