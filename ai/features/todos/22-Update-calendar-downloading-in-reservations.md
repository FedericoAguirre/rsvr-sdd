# 22. Update calendar downloading in reservations page

## User story

As an operator, I want to download the calendar with the Payment Identificador, so that I can track down the client's paid reservations.

## Acceptance criteria

Given a reservation is not associated to a payment, When the calendar is downloaded, Then the payment identifier field shows "Reservación sin asociar".
Given a set of reservations within a date range, When the calendar is downloaded, Then the description includes all existing fields plus the payment identifier.
Given a date range that spans multiple payments, When the calendar is downloaded, Then all reservations across those payments are included in the ICS file.

## Definition of Done

All tests pass, code reviewed, merged to main.
