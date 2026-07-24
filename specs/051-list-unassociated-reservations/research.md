# Research: List Unassociated Reservations on Payments Page

## Overview

Research conducted to inform the implementation of an unassociated reservations list on the client payments page, enabling staff to see which client reservations still need payment association.

## Existing Filtering Patterns

### PaymentAssociateView (`backend/apps/payments/views.py`)

The `PaymentAssociateView.get()` method already contains the pattern for finding unassociated reservations for a specific payment's client:

```python
associated_ids = payment.payment_reservations.values_list("reservation_id", flat=True)
available_reservations = Reservation.objects.filter(
    client=payment.client,
).exclude(pk__in=associated_ids).select_related(
    "equipment", "class_slot",
).order_by("-date", "class_slot__time")
```

This filter excludes reservations already linked to the current payment. The same pattern applies for the new feature, but without the payment-specific exclusion (exclude ALL reservations that have ANY PaymentReservation link).

### Reservation Model Query for "No Payment Association"

The relationship is: `Reservation.payment_links` (related_name from `PaymentReservation.reservation`, unique=True).

To find reservations with **no** PaymentReservation at all:

```python
Reservation.objects.filter(
    client_id=client_id,
    payment_links=None,
).select_related("equipment", "class_slot")
```

The `payment_links=None` filter generates a LEFT OUTER JOIN and checks for NULL on the PaymentReservation FK — equivalent to "reservations that have no related PaymentReservation row." Since `unique=True` on the FK, each reservation can have at most one link, so this approach is safe.

### Alternative: Subquery Exclusion

```python
linked_ids = PaymentReservation.objects.filter(
    reservation__client_id=client_id,
).values_list("reservation_id", flat=True)

Reservation.objects.filter(client_id=client_id).exclude(pk__in=linked_ids)
```

Both approaches work. The `payment_links=None` variant is simpler and generates a single query.

### Pagination

The existing `ClientPaymentHistoryView` paginates payments at 5 per page. For the unassociated reservations section, we can either:
- Add pagination for the reservations section separately, or
- Use the same pagination settings, or
- Show all (reasonable since most clients have a limited number of unassociated reservations)

Given typical usage (a client typically has 1-20 unassociated reservations at a time), a single non-paginated list is reasonable.

## Decision: View Extension Approach

**Decision**: Extend the existing `ClientPaymentHistoryView` to include unassociated reservations in the context, and render them in a new section of `payment_list.html`.

**Rationale**:
- No new URL or view needed — single page shows both payment history and unassociated reservations
- Reuses existing template infrastructure
- Minimal code change: add context data to existing view, add template section
- The unassociated reservations section acts as a natural action area for staff to then associate reservations with payments

**Alternatives considered**:
- New standalone view at a different URL — rejected because the user story specifies the `/payments/{client_id}` page, and keeping related functionality on one page is better UX
- Separate tab or HTMX-powered section — rejected for scope reasons; a simple static section is sufficient

## Decision: Filter Query

**Decision**: Use `Reservation.objects.filter(client_id=client_id, payment_links=None).select_related("equipment", "class_slot")` ordered by `-date, class_slot__time`.

**Rationale**:
- Single query with LEFT JOIN — efficient and simple
- `client_id` is a foreign key with existing index
- `payment_links=None` leverages Django's reverse relation filtering
- Ordering matches existing reservations list patterns

**Alternatives considered**:
- Subquery exclusion with `.exclude(pk__in=...)` — functionally equivalent but uses a subquery; the LEFT JOIN approach is more idiomatic Django

## i18n Strings Needed

- "Reservations without payment" → "Reservaciones sin pago"
- "This client has no reservations without payment." → "Este cliente no tiene reservaciones sin pago."
- "Associate" (button/link) → "Asociar"
