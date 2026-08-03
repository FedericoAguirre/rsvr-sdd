import datetime

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, models, transaction
from django.utils.translation import gettext_lazy as _


class ClassSlotManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ClassPriceQuerySet(models.QuerySet):
    def delete(self):
        raise PermissionDenied(
            _("Class price records cannot be deleted."),
        )


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

    day_of_week = models.IntegerField(
        choices=DAY_CHOICES,
        verbose_name=_("Day of week"),
    )
    time = models.TimeField(verbose_name=_("Time"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
    )

    class Meta:
        ordering = ["day_of_week", "time"]
        unique_together = ["day_of_week", "time"]
        verbose_name = _("Class slot")
        verbose_name_plural = _("Class slots")

    def __str__(self):
        day = self.get_day_of_week_display()
        time_str = self.time.strftime("%H:%M")
        status = "" if self.is_active else _(" (inactive)")
        return _("%(day)s %(time)s%(status)s") % {
            "day": day,
            "time": time_str,
            "status": status,
        }


class ClassPriceManager(models.Manager):
    def get_queryset(self):
        return ClassPriceQuerySet(self.model, using=self._db)

    def delete(self):
        raise PermissionDenied(
            _("Class price records cannot be deleted."),
        )

    def enter_price(self, class_slot, new_price, changed_by):
        return ClassPrice.enter_price(
            class_slot=class_slot,
            new_price=new_price,
            changed_by=changed_by,
        )


class ClassPrice(models.Model):
    class_slot = models.ForeignKey(
        ClassSlot,
        on_delete=models.PROTECT,
        related_name="prices",
        verbose_name=_("Class slot"),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    current = models.BooleanField(
        default=True,
        verbose_name=_("Current"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_class_prices",
        verbose_name=_("Created by"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    changed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Changed at"),
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="changed_class_prices",
        blank=True,
        null=True,
        verbose_name=_("Changed by"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    objects = ClassPriceManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Class price")
        verbose_name_plural = _("Class prices")
        constraints = [
            models.UniqueConstraint(
                fields=["class_slot"],
                condition=models.Q(current=True),
                name="unique_current_classprice_per_slot",
            ),
        ]

    def __str__(self):
        return _("%(price)s — %(slot)s") % {
            "price": self.price,
            "slot": self.class_slot,
        }

    def clean(self):
        if self.pk is not None:
            try:
                original = ClassPrice.objects.get(pk=self.pk)
            except ClassPrice.DoesNotExist:
                return
            if original.price != self.price:
                raise IntegrityError(
                    _("The price amount cannot be modified."),
                )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionDenied(
            _("Class price records cannot be deleted."),
        )

    @classmethod
    def enter_price(cls, class_slot, new_price, changed_by):
        with transaction.atomic():
            qs = cls.objects.filter(
                class_slot=class_slot,
                current=True,
            ).select_for_update(of=("self",))
            try:
                previous = qs.get()
            except cls.DoesNotExist:
                previous = None
            except cls.MultipleObjectsReturned:
                raise IntegrityError(
                    _("Multiple current prices exist for this class slot."),
                )
            if previous is not None:
                previous.current = False
                previous.changed_at = datetime.datetime.now(
                    tz=datetime.timezone.utc,
                )
                previous.changed_by = changed_by
                previous.save(
                    update_fields=["current", "changed_at", "changed_by", "updated_at"],
                )
            return cls.objects.create(
                class_slot=class_slot,
                price=new_price,
                current=True,
                created_by=changed_by,
            )
