# Use the same reservations lit format

## Description

As an Operator when accessing the /reservations webpage the reservations list shows these fields:

- Date
- Client
- Class Slot
- Equipment
- Status
- View (button)

But when I apply a filter, the reservations list shows these fields:

- Equipment
- Client
- Status

This behavior is incoherent.

The right behavior, must be to show the fields:

When the webpage first loads is to show:
- Date
- Client
- Class Slot
- Equipment
- Status
- View (button)

Whenever the page first loads, a filter is applied or cleaned.

The **Export PDF** functionality is correct. DO NOT CHANGE IT.

## Additional Requests (added during implementation)

- Implement the full fix including `reservation_list_by_slot.html` (secondary view had the same bug)
- Write TDD tests verifying all 6 columns in Spanish (Fecha, Cliente, Clase, Equipo, Estado, Ver)
- Add PDF regression tests to confirm no regressions
- Compact AI session, commit, push, and prepare PR
