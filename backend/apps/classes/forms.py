from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import ClassPrice


class ClassPriceForm(forms.ModelForm):
    class Meta:
        model = ClassPrice
        fields = ["price"]
        widgets = {
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"},
            ),
        }
        labels = {
            "price": _("Price"),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and Decimal(price) <= 0:
            raise ValidationError(
                _("Enter a positive amount."),
            )
        return price
