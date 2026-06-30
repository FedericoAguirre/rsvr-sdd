# Contracts: Duplicated Reservation Alert

**Date**: 2026-06-29

## Status

No new endpoints, URL patterns, or external interfaces are required. This feature is entirely internal to the existing `reservations/create/` page.

| Interface | Status | Notes |
|---|---|---|
| URL pattern `reservations/create/` | Unchanged | No route changes |
| ReservationForm field names and types | Unchanged | Same fields: client, equipment, class_slot, date, notes |
| Reservation model fields | Unchanged | No schema changes |
| View signature `reservation_create` | Unchanged | Handles GET (form) and POST (validation + save) |
| Authentication requirement | Unchanged | Authenticated staff only |

## Template Changes

The template `reservation_form.html` gains a non-field errors alert block:

```
{% if form.non_field_errors %}
<div class="alert alert-warning alert-dismissible fade show" role="alert">
  {% for error in form.non_field_errors %}
  <p class="mb-0">{{ error }}</p>
  {% endfor %}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
{% endif %}
```

This renders the `ValidationError` raised by the `clean()` method in `ReservationForm`. The alert follows Bootstrap 5 alert component conventions with dismissible functionality.

## Form Contract (ReservationForm.clean)

The `clean()` method raises a `ValidationError` (non-field) when a duplicate reservation is detected. The error message includes:

- Equipment name (translatable)
- Date (translatable format)
- Class slot name (translatable)
- "UNAVAILABLE" or "NO DISPONIBLE" marker

The message is wrapped with `gettext_lazy` for i18n support.

## Unchanged Contracts

| Contract | Rationale |
|---|---|
| Equipment model | No changes needed — existing ForeignKey used for lookups |
| ClassSlot model | No changes needed |
| Client model | No changes needed |
| Session/auth middleware | Reused as-is |
| i18n infrastructure | Existing Django i18n machinery reused |
