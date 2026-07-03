# Contracts: Payments Associate Button

## Modified View

### POST /payments/\<pk\>/associate/

**Existing behavior**: POST-only endpoint that associates selected reservations with a payment. Expects `reservations` (list of reservation IDs) in POST body. Returns 405 on GET.

**New behavior**: Adds a GET handler that renders a reservation selection page. POST behavior unchanged.

### GET /payments/\<pk\>/associate/

**Request**: No parameters.

**Response context**:

| Context Variable | Type | Description |
|------------------|------|-------------|
| `payment` | Payment | The payment being associated |
| `available_reservations` | QuerySet[Reservation] | Client's reservations not yet associated with this payment |
| `remaining_slots` | int | How many more reservations can be associated |

**Renders template**: `payments/payment_associate.html` (new)

### GET /payments/\<pk\>/

**Modified**: The `payment_detail.html` template now includes an **Associate** button (`<a>` tag) in the card header, placed before the Edit button.

### Tab Order

DOM source order in `payment_detail.html` card-header `<div>`:

1. Associate button `<a>` (new — first in DOM)
2. Edit button `<a>` (existing)
3. Delete form `<form>` (existing)

No `tabindex` attributes used (matches project convention).

## Modified Files

| File | Change |
|------|--------|
| `backend/apps/payments/views.py` | Add `get()` method to `PaymentAssociateView` |
| `backend/apps/payments/templates/payments/payment_detail.html` | Add Associate button `<a>` before Edit |
| `backend/apps/payments/templates/payments/payment_associate.html` | New: reservation selection page |
| `locale/es/LC_MESSAGES/django.po` | Add `Associate` key |
