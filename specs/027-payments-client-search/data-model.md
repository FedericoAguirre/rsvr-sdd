# Data Model: Payments Client Search

## Entities

### Payment (existing — no changes)

| Field | Type | Notes |
|-------|------|-------|
| client | FK → Client | Used for filtering payments via client attributes |
| ... | (all existing fields) | Unchanged |

**Key indexes**: `("client", "-date")` — supports the client-based filtering

### Client (existing — no changes)

| Field | Type | Notes |
|-------|------|-------|
| first_name | CharField | Searched via `__icontains` |
| last_name | CharField | Searched via `__icontains` |
| email | EmailField | Searched via `__icontains` |
| mobile | CharField | Searched via `__icontains` |
| is_active | BooleanField | Filter to exclude inactive clients |

## Relationships

- **Payment** belongs to **Client** (ForeignKey)
- Search flow: `q` → filter Clients by name/email/mobile → get matching Client IDs → filter Payments by those Client IDs

## No New Entities

This feature adds zero new database entities. All changes are in the view layer (query logic) and presentation layer (search UI).
