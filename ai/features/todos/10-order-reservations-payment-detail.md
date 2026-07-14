# Order reservations by date descending in payment detail

## User story

As an operator, when looking at the associated reservations in a payment detail page, I want the reservations ordered by date in descending order, so that I can quickly spot the latest one.

## Acceptance criteria

Given I'm viewing a payment detail page, when the page loads, then the associated reservations are listed sorted by date descending (most recent first).

Given I'm viewing a payment detail page with reservations on the same date, when the page loads, then those reservations are sorted by class slot time descending within the same date.

Given I'm viewing a payment detail page, when there are no associated reservations, then the list is empty (no change).

## Definition of Done

Code reviewed, tested with multiple dates, validated that latest reservation appears at the top.
