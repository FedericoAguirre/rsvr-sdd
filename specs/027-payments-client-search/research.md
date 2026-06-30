# Research: Payments Client Search

## Decision Records

### DR-001: HTMX for live search

- **Decision**: Use HTMX with 300ms debounce, matching the client search pattern
- **Rationale**: HTMX is already established in the project (clients search). It avoids adding JavaScript dependencies, enables partial page updates, and the 300ms debounce balances responsiveness with query load
- **Alternatives considered**: Standard GET form submission (slower UX, full page reloads); vanilla JS fetch (HTMX already available, no need to add more JS)

### DR-002: Single search field searches across all client attributes

- **Decision**: One text input (`q`) that searches client name, email, and mobile simultaneously
- **Rationale**: Matches the client search UX pattern. Operators don't need to choose which field to search — just type and results filter. The existing client search at `clients/search/` uses this same approach successfully
- **Alternatives considered**: Separate fields per attribute (more complex UI, clutter on the form)

### DR-003: Replace existing client ID filter with search field

- **Decision**: Replace the current `client` (numeric ID) input with the new `q` search field
- **Rationale**: The numeric ID filter is not user-friendly — operators must know the client's database ID. The new search by name/email/mobile is strictly more useful. Removing it avoids maintaining two filter mechanisms
- **Alternatives considered**: Keep both filters side by side (unnecessary complexity, violates YAGNI)

### DR-004: Exclude inactive clients from search

- **Decision**: Filter `Client.objects.filter(is_active=True)` before searching payments
- **Rationale**: Clarified in spec — soft-deleted (inactive) clients should be excluded. Only active clients' payments should appear in search results
- **Alternatives considered**: Include inactive clients (clutters results, contradicts spec)

### DR-005: i18n for all new strings

- **Decision**: All new user-facing strings use Django i18n (`{% translate %}` / `_()`)
- **Rationale**: Constitution mandates i18n for ALL user-visible strings with zero exceptions. Spanish is the only configured language

### DR-006: Test following TDD pattern

- **Decision**: New test file `tests/test_payments_search.py` with both unit and integration tests
- **Rationale**: Constitution requires TDD. Tests must be written and reviewed before implementation. Follows the pattern from previous features (e.g., specs/026-duplicated-reservation-alert)
