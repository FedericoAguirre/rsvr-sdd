from datetime import date

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

PAYMENT_TYPE_CHOICES = [
    ("CASH", _("Cash")),
    ("CC", _("Credit Card")),
    ("DC", _("Debit Card")),
    ("TRANSF", _("Electronic Transfer")),
    ("PAPP", _("Payments App")),
]


class Payment(models.Model):
    client = models.ForeignKey(
        "clients.Client", on_delete=models.PROTECT, related_name="payments",
        verbose_name=_("Client"),
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount"),
    )
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name=_("Payment type"),
    )
    payment_identifier = models.CharField(
        max_length=50, unique=True, verbose_name=_("Payment identifier"),
    )
    date = models.DateField(verbose_name=_("Date"))
    class_slot_count = models.PositiveSmallIntegerField(
        verbose_name=_("Class slot count"),
    )
    reference = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Reference"),
    )
    evidence = models.ImageField(
        upload_to="payments/evidence/", blank=True, null=True,
        verbose_name=_("Evidence"),
    )
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))
    deleted_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Deleted at"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_payments",
        verbose_name=_("Created by"),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="updated_payments",
        verbose_name=_("Updated by"),
    )

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        indexes = [
            models.Index(fields=["client", "-date"]),
            models.Index(fields=["date", "payment_type"]),
        ]

    def __str__(self):
        return _("{} – {} – {}").format(
            self.payment_identifier, self.client, self.amount,
        )

    def _generate_identifier(self):
        today_min = date(self.date.year, self.date.month, self.date.day)
        today_max = today_min
        last_today = Payment.objects.filter(
            payment_type=self.payment_type,
            date__gte=today_min,
            date__lte=today_max,
        ).exclude(pk=self.pk).order_by("payment_identifier").last()
        if last_today:
            last_seq = int(last_today.payment_identifier[-3:])
            next_seq = last_seq + 1
        else:
            next_seq = 1
        initials = (
            self.client.first_name[0].upper()
            + self.client.last_name[0].upper()
        )
        date_str = self.date.strftime("%Y%m%d")
        return f"{self.payment_type}{date_str}{initials}{next_seq:03d}"

    def save(self, *args, **kwargs):
        if not self.payment_identifier:
            self.payment_identifier = self._generate_identifier()
        super().save(*args, **kwargs)


class PaymentReservation(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payment_reservations",
        verbose_name=_("Payment"),
    )
    reservation = models.ForeignKey(
        "reservations.Reservation", on_delete=models.CASCADE,
        related_name="payment_links", unique=True,
        verbose_name=_("Reservation"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Payment Reservation")
        verbose_name_plural = _("Payment Reservations")
        indexes = [
            models.Index(fields=["payment"]),
            models.Index(fields=["reservation"]),
        ]

    def __str__(self):
        return _("{} → {}").format(
            self.payment.payment_identifier, self.reservation,
        )


