# Batch reservations from payment creation

## User story

As a system operator, I want to be able to create reservations in batch and associate them with the current payment I'm receiving, so that I can quickly create as many reservations as block classes are being paid without switching screens and doing them one by one.

## Acceptance criteria

Given I have just created a payment in `payments/create/`, when the payment is saved successfully, then a modal/pop-up appears for batch reservation creation.

Given the batch modal is open, when I view it, then it shows: a calendar, an "in service" equipment list, and the available hour slots.

Given I'm in the batch modal, when I select equipment, hour slot, and a set of days, then reservations are created and automatically associated to the current payment.

Given I'm in the batch modal, when I select days, then only dates from today up to the next Monday after the payment date are available.

Given I'm creating batch reservations, when the total would exceed 20 reservations, then the system prevents it or warns me.

Given I'm creating batch reservations, when the total would exceed 4 weeks from the payment date, then the system prevents it.

Given batch reservations were created, when I close the modal, then I'm redirected to the payment detail page showing all associated reservations.

## Workflow

1. Operator fills the payment form in `payments/create/`
2. On successful payment creation, a modal opens for batch reservations
3. Operator selects: equipment, hour slot, and batch of days
4. System creates N reservations and links them to the payment via PaymentReservation
5. Operator is redirected to the payment detail page

## Constraints

- The reservations batch size equals to the payment's block classes number
- Maximum 20 reservations per batch
- Date range: from today up to the next Monday after the payment date (within ~4 weeks)
- Only "in service" equipment shown
- Only active class slots shown
- Each reservation must respect the unique_together constraint (equipment + class_slot + date)
- Each reservation can be linked to at most one payment (PaymentReservation.reservation is unique=True)

## Definition of Done

Code reviewed, tested with edge cases (conflicting dates, max limits, equipment unavailability), validated that reservations appear correctly in the payment detail page.
