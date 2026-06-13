import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="highlight", is_safe=True)
def highlight(text, query):
    if not query or not text:
        return text
    escaped = re.escape(query)
    pattern = re.compile(f"({escaped})", re.IGNORECASE)
    result = pattern.sub(r"<mark>\1</mark>", str(text))
    return mark_safe(result)
