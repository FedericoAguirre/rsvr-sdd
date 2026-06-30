# Research: Duplicated Reservation Alert

## Technical Stack Analysis

**Language**: Python 3.12 (per `backend/pyproject.toml`)
**Framework**: Django 5.0
**Database**: PostgreSQL (via psycopg2-binary)
**Testing**: pytest with `DJANGO_SETTINGS_MODULE = "config.settings"`

## Existing Constraint Analysis

The `Reservation` model (`backend/apps/reservations/models.py`) has:

```python
unique_together = ["equipment", "class_slot", "date"]
```

This means the database already enforces uniqueness at the constraint level. When a duplicate is submitted, Django raises an `IntegrityError` or a non-field validation error during `ModelForm.is_valid()`. However, the current template (`reservation_form.html`) only renders `field.errors` — it does NOT display `form.non_field_errors()`, which is where the unique_together error appears. This explains the "silent" behavior described in the spec.

## Approach

### Detection Strategy

Two layers of detection are needed (per clarification Q1):

1. **Client-side**: Immediate feedback when the operator selects a duplicate equipment for an already-selected date + class_slot. This is a UX enhancement (instant feedback without form submission). Can be done via JavaScript or HTMX.

2. **Server-side (form validation)**: The `clean()` method on `ReservationForm` explicitly checks for existing `Reservation` records matching `[equipment, class_slot, date]` with `status=RESERVED`. This catches edge cases where the reservation state changed between page load and submit.

### Form Validation Approach

Add a `clean()` method to `ReservationForm`:

```python
def clean(self):
    cleaned_data = super().clean()
    equipment = cleaned_data.get("equipment")
    class_slot = cleaned_data.get("class_slot")
    date = cleaned_data.get("date")

    if equipment and class_slot and date:
        exists = Reservation.objects.filter(
            equipment=equipment, class_slot=class_slot, date=date,
            status="reserved",
        ).exclude(pk=self.instance.pk if self.instance else None).exists()

        if exists:
            raise ValidationError(
                _("%(equipment)s is already RESERVED for %(date)s — %(class_slot)s.")
                % {"equipment": equipment, "date": date, "class_slot": class_slot}
            )
    return cleaned_data
```

### Template Changes

The template must render `non_field_errors` to display the alert. Using Bootstrap 5 alert component:

```html
{% if form.non_field_errors %}
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    {% for error in form.non_field_errors %}
    <p class="mb-0">{{ error }}</p>
    {% endfor %}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
{% endif %}
```

### i18n Approach

- Use `gettext_lazy` from `django.utils.translation` in Python for form validation messages
- Use `{% translate %}` or `{% blocktranslate %}` template tags in templates
- The marker term "UNAVAILABLE" should be a translatable string (Spanish equivalent: "NO DISPONIBLE")
- Run `makemessages` to extract new strings, translate in Spanish `.po` file

### Client-side Detection

For the "immediate on add" requirement (Q1), a lightweight JavaScript handler can watch the equipment select field. When it changes, fetch the existing reservations for the selected date/class_slot via an API endpoint and display an inline warning before the form is submitted. This is optional but recommended for UX (handled as P3).

**Decision**: Client-side check via HTMX or plain fetch — lightweight, no additional dependency.

**Alternatives considered**: Django's built-in `validate_unique` triggers on form `is_valid()` but only shows the non-field error on submit, not on field change. Full-page reload via AJAX form submission was deemed too heavy.

## Dependencies

- None new — all dependencies already in `pyproject.toml`
- The existing `unique_together` constraint provides DB-level protection
- Django's form validation and i18n framework handle the requirements
