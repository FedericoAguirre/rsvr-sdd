# Contracts: Add Payment Button to Client Page

## Modified View

### GET /payments/create/

**Existing behavior**: Renders the payment creation form with an empty client field. Reads `?client=` from query string but does not pre-populate it into the form.

**New behavior**: When `?client=<pk>` is present in the query string, the form's client combo box is pre-selected with the specified client. Direct access (no `?client=`) retains the existing empty-client behavior.

**Request parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `client` | int | No | Client primary key to pre-select in the form |

**Response context** (unchanged):

| Context Variable | Type | Description |
|------------------|------|-------------|
| `mode` | str | Always `"create"` |
| `client_id` | str | Raw client ID from query string (existing, preserved for backward compatibility) |
| `form` | PaymentForm | The payment creation form (now with `client` field pre-populated when `?client=` is provided) |

**Renders template**: `payments/payment_form.html` (unchanged)

### GET /clients/\<pk\>/

**Modified**: The `client_detail.html` template now includes a **New Payment** button (`<a>` tag) in the action button area, placed immediately to the right of the **Nueva Reserva** button.

### Redirect Behavior

Clicking the **New Payment** button navigates to `/payments/create/?client=<pk>`, where `<pk>` is the current client's primary key.

## Tab Order

DOM source order in `client_detail.html` action button area:

1. **Nueva Reserva** button `<a>` (existing)
2. **New Payment** button `<a>` (new — placed second in DOM)
3. Other action elements (existing, unchanged)

No `tabindex` attributes used (matches project convention).

## Modified Files

| File | Change |
|------|--------|
| `backend/apps/clients/templates/clients/client_detail.html` | Add **New Payment** button `<a>` after **Nueva Reserva** |
| `backend/apps/payments/views.py` | Add `get_initial()` to `PaymentCreateView` for client pre-selection |
