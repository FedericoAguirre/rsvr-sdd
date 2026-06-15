from django import template

register = template.Library()


@register.filter
def full_name(client):
    parts = [p for p in [client.first_name, client.last_name] if p]
    return " ".join(parts) if parts else ""
