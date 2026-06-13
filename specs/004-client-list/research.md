# Research: Client List in Client Search

## Decision: Show all clients by default

**Rationale**: The current view shows `Client.objects.none()` when no search query is provided. Per the spec, when the Operator lands on `clients/search/`, they should see the full client list. The search should remain as a filter on top of the full list.

## Decision: Use Django `Paginator` for pagination

**Rationale**: Django's built-in `Paginator` class integrates cleanly with function-based views and templates. It provides page navigation, count, and per-page limits out of the box. No external pagination library needed.

**Alternatives considered**: Custom pagination via SQL `LIMIT/OFFSET` — rejected because it would duplicate Django's well-tested implementation.

## Decision: Keep search and list on the same page

**Rationale**: When a query is entered, the list filters to matching results. When no query is entered, all clients are shown. This avoids page duplication and keeps the UX simple (one URL, two modes).

## Decision: Reuse the existing counter widget from the spec

**Rationale**: The feature description mentions a "Client counter widget" already exists on the page. Research confirms the counter can be implemented as a simple `Client.objects.count()` call passed to the template.

## Decision: Edit button links to the existing admin change view

**Rationale**: The spec says "Each Client row must have a link or button to Edit that Client." The simplest path is linking to the Django admin change view (`admin:clients_client_change`) since the Client model is already registered in admin.py. Alternatively, the existing `client_detail` view could be extended, but reusing admin is faster and avoids duplication.
