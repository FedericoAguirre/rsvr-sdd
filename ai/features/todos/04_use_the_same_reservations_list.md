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