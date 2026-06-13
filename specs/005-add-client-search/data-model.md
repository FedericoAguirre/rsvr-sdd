# Data Model: Add Client Search by Name

**Date**: 2026-06-13

## Entities

### Client (existing — no schema changes)

| Field | Type | Constraints | Search relevance |
|-------|------|-------------|-----------------|
| `first_name` | `CharField(100)` | Required | Searched via `__icontains` |
| `last_name` | `CharField(100)` | Required | Searched via `__icontains` |
| `email` | `EmailField` | Unique, nullable | Already searched via `__icontains` (unchanged) |
| `mobile` | `CharField(20)` | Unique, nullable | Already searched via `__icontains` (unchanged) |
| `is_active` | `BooleanField` | Default: true | Not used in search |
| `created_at` | `DateTimeField` | Auto now add | Not used in search |
| `updated_at` | `DateTimeField` | Auto now | Not used in search |

**Default ordering**: `["last_name", "first_name"]`

## Search query logic

The combined search filter is:

```
Q(email__icontains=q) |
Q(mobile__icontains=q) |
Q(first_name__icontains=q) |
Q(last_name__icontains=q)
```

- Case-insensitive partial match on all four fields
- Minimum 3 characters enforced server-side before adding name fields to the query (email/mobile search still works with <3 chars via existing behavior)
- Results ordered by `last_name`, `first_name` (existing `Client.Meta.ordering`)

## No schema changes

The Client model remains unchanged. No new fields, tables, or migrations are required.
