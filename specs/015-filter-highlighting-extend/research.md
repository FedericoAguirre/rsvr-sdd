# Research: Extend Filter Highlighting to Email and Mobile

## Existing Implementation Analysis

### Current highlighting mechanism

- **Template tag**: `backend/apps/clients/templatetags/client_extras.py` — `@register.filter(name="highlight")`
- **Logic**: Case-insensitive regex substitution wrapping matched text in `<mark>` tags
- **Usage in template**: `_search_results.html` line 28 — `{{ c.first_name|highlight:q }} {{ c.last_name|highlight:q }}`
- **Missing**: Email (line 29) and mobile (line 30) columns do not use the `highlight` filter

### HTMX integration

- Search form in `search.html` uses `hx-trigger="keyup changed delay:300ms"` with `hx-target="#search-results"`
- View `client_search` returns either full page or partial `_search_results.html` based on `HX-Request` header
- No full-page reloads — highlighting must work in HTMX partial responses

### Mobile number normalization

**Decision**: Strip all non-numeric characters from both search term and stored mobile values before matching; highlight matched digits in the formatted display value.

**Rationale**: Mobile numbers are stored with formatting (spaces, dashes, parentheses, + prefix). Operators searching by digits should not need to match formatting characters. The existing `highlight` filter operates on the display value, so normalization must happen within the filter logic — compare normalized values, then highlight matches in the original formatted string.

**Alternatives considered**:
- Match against raw formatted string as-is → rejected because "555" would not match "+1 (555) 123-4567" (dash breaks substring)
- Normalize only stored value, require user to match format → rejected as poor UX

### Test patterns

- Existing test file: `backend/tests/test_client_search_name.py` tests name search with highlighting
- Tests use Django test client + pytest-django
- New tests needed for email and mobile highlighting behavior, including mobile number normalization cases

## Key Findings

1. Only template changes needed in `_search_results.html`
2. Template tag `client_extras.py` needs normalization logic for mobile numbers
3. No new views, models, urls, or forms required
4. New test file following existing patterns
