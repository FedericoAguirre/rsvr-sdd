from django.db import models


class ClassSlot(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
    ]
    TIME_CHOICES = [
        ("17:30", "17:30"),
        ("18:30", "18:30"),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["day_of_week", "time"]
        unique_together = ["day_of_week", "time"]

    def __str__(self):
        day = self.get_day_of_week_display()
        time_str = self.time.strftime("%H:%M")
        status = "" if self.is_active else " (inactive)"
        return f"{day} {time_str}{status}"
