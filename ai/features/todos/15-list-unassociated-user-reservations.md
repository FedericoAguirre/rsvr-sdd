# 15. List only unassociated user reservations

## User story

As a **Staff User**, I want **to get the prefiltered reservations list associated a client to show only the reservations that are not yet associated with a payment**, so that **I can quickly find and follow up on paid reservations already associated with a client**.

## Acceptance criteria

Given I accesed the `/payments/{client_id}` page, When it loads, the unassociated client's reservations automatically appear, Then the `PaymentReservation` link can be created.

Given I accesed th `/payments/{client_id}` page, When there are no matching client's reservations, Then the page shows an appropriate empty-state message.

Given I accesed the `/payments/{client_id}` page, When I create a new reservation for the payment client, Then that reservation appears in the filtered list (since it has no payment association yet).

## Definition of Done

- When a staff user enters the `/payments/{client_id}`, the client's unassociated reservations appear in the list
- The `reservation_list` view filters the queryset by `client_id=request.client_id` and excludes reservations that have a `PaymentReservation` link
- The feature integrates with actual functionallity 
- - Tests verify the filtering logic
