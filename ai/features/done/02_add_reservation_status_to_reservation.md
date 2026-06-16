# Add reservation status to a reservation

## Description

As an Administrator and Operator, I want to mark a **reservation** as "used"
when a client has assisted to the class slot.

1. The **reservation status**, can start as "reserved".
2. When the client assisted to the class slot, his reservation can be marked as "used".
3. If the client didn't assist, then the reservation can be marked as "unused".

**IMPORTANT**:

- Translate this into Spanish, for the Operator's usage
- Review the reservations use cases: list, export to pdf, filter, etc.
- Update the use cases tests for reservations and update them accordingly, pay attention to list reservation and export to pdf.

## Added During Implementation

- **Quick status management**: Add inline row actions in reservation list views for 1-click status changes, bulk operations (checkbox selection + "Mark selected as Used/Unused"), and colored status badges for at-a-glance identification. Use HTMX for instant row updates without page reloads.
