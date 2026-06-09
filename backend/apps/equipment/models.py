from django.db import models


class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ("treadmill", "Treadmill"),
        ("bike", "Stationary Bike"),
        ("elliptical", "Elliptical"),
        ("rower", "Rowing Machine"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("in-service", "In Service"),
        ("out-of-service", "Out of Service"),
    ]

    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in-service")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "equipment"

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
