from django.db import models
from django.utils.translation import gettext_lazy as _


class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ("climber", _("Climber")),
        ("treadmill", _("Treadmill")),
        ("bike", _("Stationary Bike")),
        ("elliptical", _("Elliptical")),
        ("rower", _("Rowing Machine")),
        ("other", _("Other")),
    ]
    STATUS_CHOICES = [
        ("in-service", _("In Service")),
        ("out-of-service", _("Out of Service")),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES, verbose_name=_("Equipment type"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in-service", verbose_name=_("Status"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("equipment")

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
