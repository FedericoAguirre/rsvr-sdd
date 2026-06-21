# Quickstart: Filter Highlighting Extension

## Prerequisites

- Running project (see root `README.md` or `make up`)
- Feature branch `017-filter-highlighting-extend` checked out

## What was changed

| File | Change |
|------|--------|
| `backend/apps/clients/templatetags/client_extras.py` | Mobile number normalization logic added to `highlight` filter |
| `backend/apps/clients/templates/clients/_search_results.html` | `highlight` filter applied to `c.email` and `c.mobile` cells |
| `backend/tests/test_client_search_highlighting.py` | New tests for email and mobile highlighting |

## Verification

```bash
# Run linting
ruff check backend/

# Run tests
cd backend && python -m pytest tests/test_client_search_highlighting.py -v

# Run all client-related tests
cd backend && python -m pytest tests/ -k "client" -v
```

Visit `/clients/search/` and search by email or mobile number. Matched portions should appear highlighted with `<mark>` styling.
