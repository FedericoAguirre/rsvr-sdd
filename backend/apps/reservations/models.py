from django.conf import settings
from django.db import models


class Reservation(models.Model):
    client = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="reservations"
    )
    equipment = models.ForeignKey(
        "equipment.Equipment", on_delete=models.PROTECT, related_name="reservations"
    )
    class_slot = models.ForeignKey(
        "classes.ClassSlot", on_delete=models.PROTECT, related_name="reservations"
    )
    date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_reservations",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "class_slot__time"]
        unique_together = ["equipment", "class_slot", "date"]

    def __str__(self):
        return f"{self.client} – {self.equipment} – {self.date}"
