from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassSlot(models.Model):
    DAY_CHOICES = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
    ]
    TIME_CHOICES = [
        ("17:30", _("17:30")),
        ("18:30", _("18:30")),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES, verbose_name=_("Day of week"))
    time = models.TimeField(verbose_name=_("Time"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        ordering = ["day_of_week", "time"]
        unique_together = ["day_of_week", "time"]
        verbose_name = _("Class slot")
        verbose_name_plural = _("Class slots")

    def __str__(self):
        day = self.get_day_of_week_display()
        time_str = self.time.strftime("%H:%M")
        status = "" if self.is_active else _(" (inactive)")
        return _("%(day)s %(time)s%(status)s") % {"day": day, "time": time_str, "status": status}
