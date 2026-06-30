# Quickstart: Duplicated Reservation Alert

## What

Add a visible alert on the reservation create form when an operator tries to reserve equipment that's already reserved for the same class slot and date.

## Files to Modify

### 1. `backend/apps/reservations/forms.py`

Add a `clean()` method to `ReservationForm`:

```python
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Reservation


class ReservationForm(forms.ModelForm):
    # ... existing Meta class and __init__ ...

    def clean(self):
        cleaned_data = super().clean()
        equipment = cleaned_data.get("equipment")
        class_slot = cleaned_data.get("class_slot")
        date = cleaned_data.get("date")

        if equipment and class_slot and date:
            exists = Reservation.objects.filter(
                equipment=equipment,
                class_slot=class_slot,
                date=date,
                status="reserved",
            ).exclude(pk=self.instance.pk if self.instance else None).exists()

            if exists:
                raise ValidationError(
                    _("%(equipment)s is already RESERVED for %(date)s — %(class_slot)s.")
                    % {"equipment": equipment, "date": date, "class_slot": class_slot}
                )
        return cleaned_data
```

### 2. `backend/apps/reservations/templates/reservations/reservation_form.html`

Add a non-field errors block above the form fields:

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

### 3. i18n — Translation files

Run `makemessages` to extract new strings, then add Spanish translations:

```bash
cd backend && django-admin makemessages -l es
```

Edit `backend/locale/es/LC_MESSAGES/django.po` to add Spanish translation of the alert message.

### 4. Tests

Write tests in `backend/apps/reservations/tests/`:

- **Unit test**: Test `ReservationForm.clean()` directly with a duplicate reservation
- **Integration test**: Test the full form submission flow via Django test client
- Test both English and Spanish locales for the alert message

## How to Test

1. Create a reservation with a specific equipment, class slot, and date
2. Try creating another reservation with the same equipment + class slot + date
3. The form should display a visible warning message and not submit
4. Switch to Spanish locale and repeat — alert text should appear in Spanish
