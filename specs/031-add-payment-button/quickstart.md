# Quickstart: Add Payment Button to Client Page

## What you need to know

A small feature — one button on the client detail page that navigates to the payment creation page with the client preselected.

## Files to modify

1. **`backend/apps/clients/templates/clients/client_detail.html`** — Insert `<a href="{% url 'payments:create' %}?client={{ client.pk }}" class="btn btn-success mb-3">{% translate "New Payment" %}</a>` immediately after the **Nueva Reserva** button
2. **`backend/apps/payments/views.py`** — Add `get_initial()` method to `PaymentCreateView` that pre-populates the `client` field from the `?client=` query parameter

## No database changes

No migrations. No new models. No new URL patterns.

## No new translations needed

The `"New Payment"` / `"Nuevo pago"` key already exists in `backend/locale/es/LC_MESSAGES/django.po` (lines 803-807).

## Testing

- `backend/tests/test_payments_create_button.py`: Test button presence, correct position relative to **Nueva Reserva**, correct `href` with `?client=<pk>`, client preselection on the payment form, and regression test for direct access with empty client

## Commands

```bash
ruff check backend/  # lint
pytest backend/tests/test_payments_create_button.py  # run tests
```
