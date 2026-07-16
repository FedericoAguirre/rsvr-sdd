# Research: Order Reservations by Date in Payment Detail

**Feature**: `042-order-reservations-date` | **Date**: 2026-07-14

## Overview

Research conducted to determine the implementation approach for sorting reservations by date descending in the payment detail page.

## Current Behavior

The payment detail page at `PaymentDetailView` (`backend/apps/payments/views.py:121-134`) loads associated reservations via:

```python
context["reservations"] = self.object.payment_reservations.select_related(
    "reservation__client", "reservation__equipment", "reservation__class_slot",
).all()
```

No `.order_by()` is applied. `PaymentReservation` (the through model) has no `Meta.ordering`, so the fallback is PK order (insertion order). This means reservations appear in the order they were linked to the payment, not sorted by date.

## Existing Patterns

- **Reservation model** (`backend/apps/reservations/models.py`): `Meta.ordering = ["-date", "class_slot__time"]` — descending date, then ascending class slot time.
- **PaymentAssociateView** (`backend/apps/payments/views.py`): queries `Reservation` directly and uses `.order_by("-date", "class_slot__time")`.
- **PaymentDetailView** queries through `PaymentReservation` (via the `payment_reservations` related manager), so field lookups must traverse the FK: `-reservation__date`, `-reservation__class_slot__time`.

## Decision

Add `order_by("-reservation__date", "-reservation__class_slot__time")` to the PaymentDetailView queryset.

- **Rationale**: Matches existing ordering patterns in the same app. Uses Django ORM's built-in ordering with related field lookups. Single query, no N+1.
- **Alternatives considered**: Adding `Meta.ordering` to `PaymentReservation` — rejected because it would affect all queries and couples ordering to the through model rather than the view's specific needs. Applying ordering in the template — rejected because it violates separation of concerns (ordering should happen at the query level).

## Secondary Sort

Per FR-002, same-date reservations must be sorted by class slot time descending. The `PaymentAssociateView` uses ascending time as secondary sort. For consistency with the spec (most recent first — latest time first), we use **descending** time: `-reservation__class_slot__time`.

## Testing Approach

Add assertions to the existing `test_payment_detail_shows_associated_reservations` test to verify:
1. Reservations appear in correct order (date descending, then time descending)
2. The response is 200 and contains expected data

## Affected Files

| File | Change |
|------|--------|
| `backend/apps/payments/views.py:130` | Add `.order_by("-reservation__date", "-reservation__class_slot__time")` to queryset |
| `backend/tests/test_payments.py` | Add ordering assertions to existing test or create new test |
