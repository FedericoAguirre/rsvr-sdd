from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("reserved", _("Reserved")),
        ("used", _("Used")),
        ("unused", _("Unused")),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="reserved",
        verbose_name=_("Status"),
    )
    client = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="reservations",
        verbose_name=_("Client"),
    )
    equipment = models.ForeignKey(
        "equipment.Equipment", on_delete=models.PROTECT, related_name="reservations",
        verbose_name=_("Equipment"),
    )
    class_slot = models.ForeignKey(
        "classes.ClassSlot", on_delete=models.PROTECT, related_name="reservations",
        verbose_name=_("Class slot"),
    )
    date = models.DateField(verbose_name=_("Date"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_reservations",
        verbose_name=_("Created by"),
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "class_slot__time"]
        unique_together = ["equipment", "class_slot", "date"]
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return _("%(client)s – %(equipment)s – %(date)s") % {"client": self.client, "equipment": self.equipment, "date": self.date}
