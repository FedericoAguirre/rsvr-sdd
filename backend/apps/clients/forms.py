from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Client


class ClientSearchForm(forms.Form):
    q = forms.CharField(
        label=_("Search by email or mobile"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Search clients..."), "id": "id_q"}),
    )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["first_name", "last_name", "email", "mobile"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
        }
