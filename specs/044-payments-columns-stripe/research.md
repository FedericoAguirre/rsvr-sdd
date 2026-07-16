# Research: Payments Columns Stripe

## Overview

This feature reorders columns and adds striping to the "Reservas asociadas" grid on the payment detail page. No technical unknowns exist — the implementation is a single Django template change.

## Findings

### Column Order Change

**Decision**: Reorder `<th>` elements from `Date/Equipment/Class Slot/Status` to `Class Slot/Date/Equipment/Status` and align `<td>` elements correspondingly.

**Rationale**: Matches the same pattern established in feature 043 on the client detail page. Reuses existing `{% translate %}` tags — no new i18n entries needed.

### Striped Rows

**Decision**: Add `table-striped` class to the `<table>` element.

**Rationale**: The project uses Bootstrap 5, which provides `.table-striped` as a built-in CSS class. No custom CSS required. The same pattern is used by other tables in the project (e.g., `13-stripped-table-reservations-pdf`).

### Alternatives Considered

- Custom CSS stripe: Rejected — Bootstrap's `.table-striped` is the project convention and simpler.

## Dependencies

| Dependency | Purpose | Already Present |
|------------|---------|-----------------|
| Bootstrap 5 | `.table-striped` class | ✅ Yes |
| Django i18n | `{% translate %}` tags for headers | ✅ Yes |

## Risks

None identified. This is a purely cosmetic change with no impact on data, logic, or behavior.
