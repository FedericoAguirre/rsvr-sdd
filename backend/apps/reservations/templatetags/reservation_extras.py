from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def full_name(client):
    parts = [p for p in [client.first_name, client.last_name] if p]
    return " ".join(parts) if parts else ""


@register.filter
def status_badge_class(status):
    mapping = {
        "reserved": "badge bg-success",
        "used": "badge bg-primary",
        "unused": "badge bg-secondary",
    }
    return mapping.get(status, "badge bg-secondary")


@register.filter
def status_label(status):
    mapping = {
        "reserved": _("Reserved"),
        "used": _("Used"),
        "unused": _("Unused"),
    }
    return mapping.get(status, status)
