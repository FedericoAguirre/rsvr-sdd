from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.classes.models import ClassSlot
from apps.equipment.models import Equipment

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["client", "equipment", "class_slot", "date", "notes"]
        labels = {
            "client": _("Client"),
            "equipment": _("Equipment"),
            "class_slot": _("Class slot"),
            "date": _("Date"),
            "notes": _("Notes"),
        }
        widgets = {
            "client": forms.Select(attrs={"class": "form-control"}),
            "equipment": forms.Select(attrs={"class": "form-control"}),
            "class_slot": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].queryset = Equipment.objects.filter(status="in-service")
        self.fields["class_slot"].queryset = ClassSlot.objects.filter(is_active=True)

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
                    _("%(equipment)s is UNAVAILABLE for %(date)s — %(class_slot)s (already reserved).")
                    % {"equipment": equipment, "date": date, "class_slot": class_slot}
                )
        return cleaned_data
