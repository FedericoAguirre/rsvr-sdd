# Research: Consistent Reservations List

## Bug Analysis

The inconsistency is in `backend/apps/reservations/templates/reservations/reservation_list.html`:

- **Unfiltered state** (no `class_slot` in querystring, line 61-77): renders a full table with 6 columns: Date, Client, Class, Equipment, Status, and a View button.
- **Filtered state** (`class_slot` present, line 42-60): renders a reduced table with only 3 columns: Equipment, Client, Status.

This happens because the template branches on `{% if class_slot %}` and renders entirely different `<table>` blocks rather than conditionally controlling column visibility.

The separate `reservation_list_by_slot.html` template (used by the `reservation_list_by_slot` view) has the same reduced 3-column layout.

## Root Cause

The template uses a structural conditional (`{% if class_slot %}`) to switch between two completely separate table definitions, and the "filtered" branch was defined with fewer columns. This is not a backend or view issue — the `reservation_list` view returns the same `Reservation` queryset in both cases, with the same related fields available.

## Fix Approach

**Decision**: Unify the template to always render all 6 columns. Remove the `{% if class_slot %}` branching that swaps the table definition.

Changes needed in `reservation_list.html`:
1. Remove the `{% if class_slot %}...{% else %}...{% endif %}` branch around the table
2. Always render the full 6-column table with Date, Client, Class Slot, Equipment, Status, View button
3. Keep the header/info section above the table (date display, Export PDF button) conditionally visible when a slot is selected
4. Keep the filter form and empty state as-is

The `reservation_list_by_slot.html` template should also be updated to show all 6 columns for consistency.

## Dependencies

- No new Python packages
- No database migrations
- No view/URL changes
- Export PDF (`reservation_list_pdf.html`) must not be modified

## Alternatives Considered

- **CSS-based column toggling**: More complex, error-prone. The template should just always render the columns.
- **Backend change**: Not needed — the view already passes all required data.

## Decisions

| Decision | Rationale |
|----------|-----------|
| Fix templates only | No backend changes required; views already provide full data |
| Unify to 6-column table | Simplest fix; matches user expectation from spec |
| Update both templates | Both `reservation_list.html` and `reservation_list_by_slot.html` have the same issue |
| Do NOT touch PDF template | Export PDF is explicitly out of scope per FR-004 |
