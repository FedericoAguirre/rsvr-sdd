from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "client", "amount", "payment_type", "payment_identifier",
            "date", "class_slot_count", "reference", "evidence", "notes",
        ]
        widgets = {
            "client": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_type": forms.Select(attrs={"class": "form-control"}),
            "payment_identifier": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d",
            ),
            "class_slot_count": forms.NumberInput(attrs={"class": "form-control"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
            "evidence": forms.FileInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get("instance"):
            self.fields["date"].initial = date.today()
        self.fields["payment_identifier"].required = False
        self.fields["payment_identifier"].help_text = _(
            "Leave empty for auto-generation",
        )
        instance = kwargs.get("instance")
        if instance and instance.pk:
            # Only allow editing reference, notes, evidence
            for field in ["client", "amount", "payment_type",
                          "payment_identifier", "date", "class_slot_count"]:
                self.fields[field].disabled = True
            formatted = f"${float(instance.amount):,.2f}"
            self.fields["amount"] = forms.CharField(
                initial=formatted, disabled=True, required=False,
                label=self.fields["amount"].label,
            )
            self.fields["evidence"].required = False

    def clean_evidence(self):
        evidence = self.cleaned_data.get("evidence")
        if evidence:
            if evidence.size > 5 * 1024 * 1024:
                raise ValidationError(_("File too large. Max 5 MB."))
            if evidence.content_type not in ("image/jpeg", "image/png"):
                raise ValidationError(_("Only JPEG and PNG images are allowed."))
        return evidence

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise ValidationError(_("Amount must be positive."))
        return amount

    def clean_class_slot_count(self):
        count = self.cleaned_data.get("class_slot_count")
        if count is not None and count < 1:
            raise ValidationError(_("Class slot count must be at least 1."))
        return count
