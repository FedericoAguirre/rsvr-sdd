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


class ClientCsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label=_("CSV file"),
        help_text=_("Upload a CSV file with columns: first_name, last_name, email, mobile."),
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".csv"}),
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get("csv_file")
        if file:
            if not file.name.endswith(".csv"):
                raise forms.ValidationError(_("Only .csv files are allowed."))
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_("File size must be less than 5 MB."))
        return file
