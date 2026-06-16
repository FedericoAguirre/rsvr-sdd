from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Equipment


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["name", "equipment_type", "status", "notes"]
        labels = {
            "name": _("Name"),
            "equipment_type": _("Equipment type"),
            "status": _("Status"),
            "notes": _("Notes"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "equipment_type": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
