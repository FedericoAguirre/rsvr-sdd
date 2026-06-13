# Contract: Client Search Endpoint

**Endpoint**: `GET /clients/search/`
**View name**: `clients:client-search`
**Auth**: `@login_required`

## Query parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | No | Search query — matches against email, mobile, first_name, and last_name (case-insensitive partial match) |
| `page` | integer | No | Page number for pagination (default: 1) |

## Response behavior

### Full page request (no HX-Request header)

Returns the full HTML page with search form, results table, pagination, and client counter.

### HTMX partial request (HX-Request header present)

Returns only the `_search_results.html` partial containing:
- The results table body
- Pagination controls
- "Client NOT FOUND" alert if no results match the query

## Search logic

```
filter = Q(email__icontains=q) | Q(mobile__icontains=q)
if len(q) >= 3:
    filter |= Q(first_name__icontains=q) | Q(last_name__icontains=q)
```

- Minimum 3 characters for name search (email/mobile search works with any length)
- Case-insensitive across all fields
- Results sorted by `last_name`, `first_name`

## Highlighting

Matched portions of `first_name` and `last_name` are wrapped in `<mark>` tags server-side. The `<mark>` element is styled with bold text and a background color per Bootstrap defaults.

## Error states

| Condition | Response |
|-----------|----------|
| No results match query | "Client NOT FOUND" alert in results partial |
| No clients in database | "No clients found." message (existing behavior) |
| Query < 3 chars | Falls back to email/mobile-only search (no name search) |
