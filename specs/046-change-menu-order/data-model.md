# Data Model: Change navigation bar menu order

**Status**: No new entities introduced.

This feature modifies the presentation order of existing navigation menu items only. No data model changes are required.

## Existing Entities Referenced

| Entity | Usage | Impact |
|--------|-------|--------|
| `User` (auth) | Controls conditional nav visibility (`is_superuser`, `perms`) | Unchanged |
| URL routes | `reservations:reservation-list`, `clients:client-search`, etc. | Unchanged — only `<li>` order changes |

## State Transitions

None. The nav order is static — no runtime state changes.
