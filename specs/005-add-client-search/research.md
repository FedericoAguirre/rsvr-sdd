# Research: Add Client Search by Name

**Phase**: 0 — Outline & Research
**Date**: 2026-06-13

## Decisions

### Search implementation approach

- **Decision**: Extend existing `client_search` view filter to include name fields
- **Rationale**: Reuses the existing view, template, pagination, and counter. No new URL or view needed. The existing `Q(email__icontains=q) | Q(mobile__icontains=q)` filter is extended with `| Q(first_name__icontains=q) | Q(last_name__icontains=q)`.
- **Alternatives considered**: Separate endpoint for name search — rejected because it would duplicate pagination, counter, and template logic.

### Dynamic search (HTMX)

- **Decision**: Use HTMX loaded from CDN for real-time search with debounce
- **Rationale**: HTMX enables partial page updates without writing custom JS. The existing search form gets `hx-get`, `hx-trigger="keyup changed delay:300ms"`, and `hx-target="#search-results"`. A new partial template `_search_results.html` is swapped in on each keystroke.
- **Alternatives considered**: Vanilla JS fetch — rejected because HTMX is simpler and matches the spec's HTMX recommendation. Django Channels/WebSockets — overkill for this use case.

### Highlighting matched text

- **Decision**: Server-side string replacement using `mark_safe` + template filter to wrap matched portions in `<mark>` tags, styled with Bootstrap's `mark` class (bold + background color)
- **Rationale**: Server-side highlighting avoids CORS issues, works without JS, and integrates naturally with Django template rendering.
- **Alternatives considered**: Client-side JS highlighting — rejected because HTMX replaces the entire partial, which would clear JS-applied highlights.

### Sorting

- **Decision**: Alphabetical by first_name, then last_name (matching existing `Client.Meta.ordering`)
- **Rationale**: Already the default ordering on the Client model. Consistent with existing behavior.

### Accessibility

- **Decision**: Follow WCAG 2.1 AA
- **Rationale**: The `<mark>` element is semantically correct for highlighted text and is announced by screen readers. HTMX triggers `aria-live` regions should be added to the search results container for dynamic content announcements.

## Dependencies

- **HTMX**: Added via `<script>` tag in base.html (no Python package needed)

## Technology choices

| Tech | Decision | Rationale |
|------|----------|-----------|
| HTMX version | Latest (2.x) via CDN | Simplest integration, no build step |
| Highlight element | HTML5 `<mark>` tag | Semantic, accessible, styled by default |
| Debounce mechanism | HTMX `delay:300ms` modifier | Built into HTMX trigger spec |
| Minimum chars check | Server-side in view | Prevents empty/queries <3 chars from being sent |

## Integration patterns

| Integration | Pattern | Notes |
|-------------|---------|-------|
| HTMX + Django | Standard `hx-get` with partial template | View checks `request.headers.get("HX-Request")` to return full page vs partial |
| Existing search + name search | Combined OR filter | Single `q` parameter searches email, mobile, first_name, last_name simultaneously |
