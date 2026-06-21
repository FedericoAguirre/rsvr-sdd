# Data Model: Filter Highlighting Extension

No new entities, fields, or relationships are introduced by this feature. This is a presentation-layer change only.

## Reference: Client Entity

Defined in `backend/apps/clients/models.py`. Fields relevant to this feature:

| Field | Type | Purpose |
|-------|------|---------|
| `email` | EmailField | Display + search in email column |
| `mobile` | CharField | Display + search in mobile column (formatted, may contain `+`, spaces, dashes, parentheses) |
| `first_name` | CharField | Already highlighted; reference for highlight behavior |
| `last_name` | CharField | Already highlighted; reference for highlight behavior |

## Data Flow

```
User types query → View filters via Q(email__icontains=q) | Q(mobile__icontains=q)
  → Template applies |highlight:q filter
    → For email: regex substring match (case-insensitive)
    → For mobile: strip non-numeric, match digits substring, highlight in formatted string
```
