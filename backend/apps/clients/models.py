from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_("Email"))
    mobile = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name=_("Mobile"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        parts = [self.first_name, self.last_name]
        contact = self.email or self.mobile or "no contact"
        return f"{' '.join(parts)} ({contact})"

    def clean(self):
        if not self.email and not self.mobile:
            from django.core.exceptions import ValidationError
            raise ValidationError("At least one of email or mobile is required.")
