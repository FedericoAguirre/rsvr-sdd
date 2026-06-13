# Quickstart: Add Client Search by Name

## Prerequisites

- Working Django development environment
- Existing clients/search/ page with Client model data
- Test database with sample clients

## What changes

1. **`backend/apps/clients/views.py`** — Extend search filter to include `first_name` and `last_name`; return HTMX partial when `HX-Request` header is present
2. **`backend/apps/clients/templates/clients/search.html`** — Add `hx-get`, `hx-trigger`, `hx-target` attributes to the search form; include the results partial
3. **`backend/apps/clients/templates/clients/_search_results.html`** — NEW partial template for HTMX swaps (results table + pagination + alerts)
4. **`backend/templates/base.html`** — Add HTMX script tag from CDN
5. **`backend/tests/test_client_search_name.py`** — NEW tests for name search, highlighting, "Client NOT FOUND"

## Verify

```bash
cd backend
pytest tests/test_client_search_name.py -v
```

## Test scenarios

- Search by first name (partial, case-insensitive)
- Search by last name (partial)
- Search with <3 chars does NOT trigger name search
- Existing email and mobile search still work
- "Client NOT FOUND" message appears when no match
- Matched text is highlighted with `<mark>` tags
- HTMX partial responses return only the results section
