# Quickstart: List Unassociated Reservations on Payments Page

## Prerequisites

- Docker Compose running (`make up` or `docker compose up -d`)
- Django migrations applied (`docker compose exec web uv run manage.py migrate`)
- Existing test database with `Reservation`, `Payment`, and `PaymentReservation` data

## Implementation Steps

### 1. Extend View Context

In `backend/apps/payments/views.py`, modify `ClientPaymentHistoryView`:

- Import `Reservation` from `apps.reservations.models`
- Add `unassociated_reservations` to `get_context_data`:
  - Query: `Reservation.objects.filter(client_id=..., payment_links=None).select_related("equipment", "class_slot").order_by("-date", "class_slot__time")`
  - No pagination (all unassociated reservations shown)

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["client_filter"] = str(self.kwargs["client_id"])
    from apps.reservations.models import Reservation
    context["unassociated_reservations"] = Reservation.objects.filter(
        client_id=self.kwargs["client_id"],
        payment_links=None,
    ).select_related("equipment", "class_slot").order_by("-date", "class_slot__time")
    return context
```

### 2. Update Template

In `backend/apps/payments/templates/payments/payment_list.html`, add a new section after the payment results:

- Section heading: "Reservations without payment" (translatable)
- Table or card list showing: date, class slot, equipment, status
- Empty state message when no unassociated reservations exist

### 3. i18n

- Extract new strings: `docker compose exec web uv run manage.py makemessages -l es`
- Translate strings in `backend/locale/es/LC_MESSAGES/django.po`
- Compile: `docker compose exec web uv run manage.py compilemessages`

### 4. Tests

Create `backend/tests/test_payments_unassociated_reservations.py`:

- Test that unassociated reservations appear on the page
- Test that associated reservations do NOT appear
- Test empty state when all reservations are associated
- Test empty state when client has no reservations at all
- Test that existing payment history list is unaffected

## Verification

```bash
# Run tests for this feature
docker compose exec web uv run pytest backend/tests/test_payments_unassociated_reservations.py -v

# Run full test suite
docker compose exec web uv run pytest

# Compile translations
docker compose exec web uv run manage.py compilemessages
```
