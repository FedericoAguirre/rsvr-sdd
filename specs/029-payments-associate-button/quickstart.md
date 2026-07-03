# Quickstart: Payments Associate Button

## What you need to know

A simple feature — one button on the payment detail page that navigates to the payment-reservation association page.

## Files to modify

1. **`backend/apps/payments/views.py`** — Add `get()` method to `PaymentAssociateView` that renders a new template with the client's available reservations
2. **`backend/apps/payments/templates/payments/payment_detail.html`** — Insert `<a href="{% url 'payments:associate' payment.pk %}">` button before the Edit button in the card header
3. **`backend/apps/payments/templates/payments/payment_associate.html`** — New file: form listing the client's reservations with checkboxes, POSTing to the same URL
4. **`locale/es/LC_MESSAGES/django.po`** — Add `Associate` → `Asociar`

## No database changes

No migrations. No new models. No new URL patterns.

## Testing

- `test_payments_associate_button.py`: Test button presence, correct position relative to Edit, correct href, correct tab order
- Template test: GET `/payments/<pk>/associate/` returns 200 with available reservations
- POST test: existing `PaymentAssociateView` behavior remains unchanged

## Commands

```bash
ruff check backend/  # lint
pytest backend/tests/test_payments_associate_button.py  # run tests
```
