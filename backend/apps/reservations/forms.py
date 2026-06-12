from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Reservation
from apps.equipment.models import Equipment
from apps.classes.models import ClassSlot
from apps.clients.models import Client


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
