# Duplicated reservation alert message

As an operator I want to receive an alert message, when trying to reserve an already reserved equipment in the same class slot and date.

The reservations/create/ webpage does not allow to duplicate a equipment in reservations, but it does it silently.

I want the alert to show the date, class slot and equipment mark as UNAVAILABLE, when the reservations status is RESERVED.

## Acceptance criteria

- When trying to reserve an already reserved equipment in the same class slot and date an alert is shown.
- The alert show the next data: the date, class slot and equipment mark as UNAVAILABLE.
- The alert tags and related text as translated into Spanish.
- The i18n assets are updated accordingly.
- The alert message is designed using the UX best practices.
