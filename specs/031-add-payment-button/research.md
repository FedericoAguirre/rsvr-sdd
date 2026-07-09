# Research: Add Payment Button to Client Page

## Phase 0 — Findings

### Decision: New Payment Button Style

**Decision**: `btn btn-success mb-3` — matching the `btn-success` variant already used for the **Download Calendar** button on the same page, ensuring visual consistency with existing action buttons.

**Rationale**:
- The client detail page already uses `btn-primary` for **Nueva Reserva** and `btn-success` for **Download Calendar**
- Using `btn-success` for **New Payment** maintains the color-coded action button pattern already established
- The `mb-3` (margin-bottom) class matches the existing **Nueva Reserva** button for vertical alignment consistency
- A solid color button is more prominent than an outline variant, appropriate for a primary navigation action

**Alternatives considered**:
- `btn btn-outline-success` (rejected: outline variants are used for secondary actions like Associate in other parts of the project)
- `btn btn-primary` (rejected: would be indistinguishable from the adjacent **Nueva Reserva** button)

### Decision: Client Preselection Mechanism

**Decision**: Override `get_initial()` in `PaymentCreateView` to set the `client` field initial value from the `?client=` query parameter. The standard `forms.Select` widget for the `client` field (using `class="form-control"`) will render the preselected value without any additional template changes.

**Rationale**:
- The existing `PaymentCreateView` already reads `?client=` in `get_context_data()` but does not pre-populate the form
- Django's `CreateView` + `ModelForm` automatically handles ForeignKey field initialization via `get_initial()`
- No changes needed to `PaymentForm`, `payment_form.html`, or URL patterns
- Direct access (no `?client=` parameter) leaves the field empty by default, satisfying FR-005

**Alternatives considered**:
- Passing `client_id` in the URL path (e.g., `payments/create/<int:client_id>/`) — rejected: would require new URL pattern and changes more files
- Using session storage to pass the client ID — rejected: unnecessary complexity for simple GET parameter passing

### Decision: i18n for Button Label

**Decision**: Use `{% translate "New Payment" %}` in the template. The translation key `"New Payment"` / `"Nuevo pago"` already exists in `backend/locale/es/LC_MESSAGES/django.po` (lines 803-807), so no new translation entry is needed.

**Rationale**:
- The existing translation key is already registered and translated
- No new `.po` file changes required
- Consistent with the existing i18n pattern used for **Nueva Reserva** (`{% translate "New Reservation" %}`)

**Alternatives considered**:
- Creating a new translation key (rejected: unnecessary — key already exists)

### Decision: Button Placement

**Decision**: Place the **New Payment** `<a>` tag immediately after the **Nueva Reserva** `<a>` tag in the template DOM. No `tabindex` attributes — DOM source order determines tab order, matching the project convention.

**Rationale**:
- The spec explicitly states "right of the **Nueva Reserva** button"
- The existing buttons already use DOM-source-order for left-to-right placement
- No `tabindex` is used anywhere in the project, maintaining consistency

### Decision: Test Structure

**Decision**: New test file `backend/tests/test_payments_create_button.py` covering:
1. Button presence on client detail page (GET `clients/<pk>/`)
2. Button position relative to **Nueva Reserva** (DOM order check)
3. Correct `href` with `?client=<pk>` query parameter
4. Clicking the button navigates to `payments/create/?client=<pk>` and the form pre-selects the client
5. Direct access to `payments/create/` shows empty client field (regression test)
