from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Payment


class PaymentSearchForm(forms.Form):
    q = forms.CharField(
        label=_("Search by client"),
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Search by client name, email or mobile..."),
                "id": "id_q",
            },
        ),
    )


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
        if count is not None and count > 20:
            raise ValidationError(_("Class slot count cannot exceed 20."))
        return count


class BatchReservationForm(forms.Form):
    payment_id = forms.IntegerField()
    equipment_id = forms.IntegerField()
    class_slot_id = forms.IntegerField()
    dates = forms.JSONField()

    def clean_equipment_id(self):
        from apps.equipment.models import Equipment
        eid = self.cleaned_data["equipment_id"]
        try:
            equipment = Equipment.objects.get(pk=eid, status="in-service")
        except Equipment.DoesNotExist:
            raise ValidationError(_("Selected equipment is not available."))
        return equipment

    def clean_class_slot_id(self):
        from apps.classes.models import ClassSlot
        sid = self.cleaned_data["class_slot_id"]
        try:
            slot = ClassSlot.objects.get(pk=sid, is_active=True)
        except ClassSlot.DoesNotExist:
            raise ValidationError(_("Selected class slot is not available."))
        return slot

    def clean_dates(self):
        from apps.classes.models import ClassSlot
        from apps.payments.models import Payment
        from apps.reservations.models import Reservation
        from django.db.models import Max
        from datetime import date, timedelta
        raw = self.cleaned_data["dates"]
        pid = self.cleaned_data.get("payment_id")
        payment = Payment.objects.filter(pk=pid).first()
        if not payment:
            raise ValidationError(_("Payment not found."))
        block_count = payment.class_slot_count
        parsed = []
        for d in raw:
            try:
                parsed.append(date.fromisoformat(d))
            except (ValueError, TypeError):
                raise ValidationError(_("Invalid date format: {}.").format(d))
        if len(parsed) != block_count:
            raise ValidationError(
                _("Must select exactly {} dates.").format(block_count),
            )
        if len(parsed) > 20:
            raise ValidationError(_("Cannot create more than 20 reservations at once."))
        if len(set(parsed)) != len(parsed):
            raise ValidationError(_("Duplicate dates are not allowed."))
        raw_start = payment.date
        latest = Reservation.objects.filter(client=payment.client).aggregate(Max("date"))
        if latest["date__max"] is not None:
            raw_start = max(raw_start, latest["date__max"] + timedelta(days=1))
        next_monday = raw_start + timedelta(days=(7 - raw_start.weekday()) % 7 or 7)
        end = next_monday + timedelta(weeks=4)
        for d in parsed:
            if d < next_monday or d > end:
                raise ValidationError(
                    _("Date {} is outside the allowed range.").format(d),
                )
        slot = self.cleaned_data.get("class_slot_id")
        if isinstance(slot, ClassSlot):
            for d in parsed:
                if not ClassSlot.objects.filter(
                    day_of_week=d.weekday(), time=slot.time, is_active=True,
                ).exists():
                    raise ValidationError(
                        _("No class slot at {} for date {}.").format(slot.time, d),
                    )
        return parsed
