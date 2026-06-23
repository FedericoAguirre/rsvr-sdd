# Research: Quick Reservation Status Management

## Unknowns Resolved

No NEEDS CLARIFICATION markers existed in the spec. All technical decisions were derived from existing project patterns.

### Decision 1: HTMX Integration Pattern
- **Decision**: Use `django-htmx` package to detect HTMX requests via `request.htmx` attribute
- **Rationale**: Standard Django HTMX integration. The project already loads HTMX 2.0 from CDN in `base.html`. The existing `reservation_change_status` view will return a partial template fragment when `request.htmx` is active, and the existing redirect (to detail page) for non-HTMX requests.
- **Alternatives considered**: Manual `HX-Request` header check — possible but unnecessary given `django-htmx` is the community-standard approach.

### Decision 2: HTMX Partial Response
- **Decision**: Return rendered `partials/reservation_row.html` template when the request comes via HTMX; redirect as before for non-HTMX requests.
- **Rationale**: HTMX swaps the full row (`tr#row-{{ pk }}`) so the entire row content (including badges and buttons) is replaced. This keeps the view simple and consistent.
- **Alternatives considered**: Returning JSON and updating via JavaScript — adds unnecessary complexity since HTMX handles HTML swapping natively.

### Decision 3: Status Badge Colors via Bootstrap
- **Decision**: Map status values to Bootstrap badge classes:
  - `reserved` → `badge bg-success` (green)
  - `used` → `badge bg-primary` (blue)
  - `unused` → `badge bg-secondary` (gray)
- **Rationale**: Bootstrap 5.3 is already loaded. These classes provide accessible, consistent coloring. A template tag filter (`status_badge_class`) will encapsulate the mapping.
- **Alternatives considered**: Custom CSS classes — would duplicate Bootstrap's color system; inline styles — harder to maintain.

### Decision 4: Inline Action Button Visibility
- **Decision**: Show both "used" and "unused" buttons on every row, disabling/hiding the button matching the current status.
- **Rationale**: Consistent UI — operators always know where to find both actions. The current status's button is hidden or disabled to prevent no-op submissions.
- **Alternatives considered**: Show only the applicable action (e.g., only "Mark as used" if status is reserved) — could be confusing if operator needs to change to the other status.

### Decision 5: Error Handling for Failed Requests
- **Decision**: Use HTMX's built-in error handling — if the server returns a non-200 status, HTMX will not swap the content. Add a toast/alert area within each row for error messages returned by the server.
- **Rationale**: HTMX natively handles swap-on-success. For errors, the view returns an error partial with a message, or a 4xx/5xx status that HTMX surfaces via `htmx:responseError` event.
- **Alternatives considered**: Custom JavaScript — more complex and fragile; HTMX's native behavior is sufficient.
