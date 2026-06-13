# Data Model: Client List Feature

**No schema changes required.** This feature only reads existing data.

## Existing Entity

### Client

| Field | Type | Notes |
|-------|------|-------|
| `first_name` | CharField | Displayed in list |
| `last_name` | CharField | Displayed in list |
| `email` | EmailField (nullable) | Displayed in list |
| `mobile` | CharField (nullable) | Displayed in list |
| `is_active` | BooleanField | Displayed in list |
| `created_at` | DateTimeField | Displayed in list |
| `updated_at` | DateTimeField | Displayed in list |

## New Queries

| Query | Purpose | Frequency |
|-------|---------|-----------|
| `Client.objects.all()[:10]` (paginated) | Display current page of clients | Every page load (search mode) |
| `Client.objects.filter(email/mobile__icontains=q)[:10]` (paginated) | Display filtered results (search mode) | On search submit |
| `Client.objects.count()` | Counter widget value | Every page load |

## No New Entities

All data already exists in the Client model. No migrations required.
