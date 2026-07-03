# Research: Payments Associate Button

## Phase 0 — Findings

### Decision: Associate Button Behavior

**Decision**: Adding an `<a>` link that navigates to `payments/<pk>/associate/` + adding a GET handler to `PaymentAssociateView`.

**Rationale**:
- FR-003 explicitly states the button must navigate to the associate URL (implying a GET link, not POST)
- The existing `PaymentAssociateView` is POST-only and returns 405 on GET
- All action buttons in `payment_detail.html` follow the same DOM-order pattern
- Adding a GET handler and a template for selecting reservations completes the missing UI for the association flow that spec 022 started but left incomplete (T046 was never implemented)

**Alternatives considered**:
- Making the button POST directly (rejected: contradicts FR-003, and the POST view expects reservation IDs that the user must select first)
- Using a modal instead of a page (rejected: simpler to follow the existing page-based pattern)

### Decision: Button Style

**Decision**: `btn btn-sm btn-outline-info` — a distinct color from Edit (`btn-outline-primary`) and Delete (`btn-outline-danger`).

**Rationale**: The project consistently uses color-coded action buttons. No `btn-outline-info` is currently used for actions, making it visually distinct.

**Alternatives considered**:
- `btn-outline-secondary` (rejected: too close to Cancel buttons)
- `btn-outline-success` (rejected: implies completion, not navigation)

### Decision: Tab Order

**Decision**: No `tabindex` attributes — DOM source order is the sole determinant, matching the existing pattern in the project.

**Rationale**: The project uses zero `tabindex` attributes. The Associate button's `<a>` tag will be placed before the Edit `<a>` tag in the template DOM, giving it the correct focus order naturally.

### Decision: Associate Page Template

**Decision**: New template `payment_associate.html` rendered by the GET handler.

**Rationale**: A full page listing the client's reservations with checkboxes is more discoverable and follows the project's page-per-action pattern better than a modal.

### Decision: Associate Button Translation Key

**Decision**: Use `{% translate "Associate" %}` with the key `Associate` and Spanish translation `Asociar`.

**Rationale**: Matches the existing i18n pattern (simple, consistent key naming). "Asociar" is the standard Spanish term for this action.
