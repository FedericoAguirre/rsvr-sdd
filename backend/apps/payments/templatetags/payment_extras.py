from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def payment_type_label(value):
    labels = {
        "CASH": _("Cash"),
        "CC": _("Credit Card"),
        "DC": _("Debit Card"),
        "TRANSF": _("Electronic Transfer"),
        "PAPP": _("Payments App"),
    }
    return labels.get(value, value)


@register.filter
def currency(value):
    """Format a number as $#,###.## regardless of locale."""
    if value is None:
        return ""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)
