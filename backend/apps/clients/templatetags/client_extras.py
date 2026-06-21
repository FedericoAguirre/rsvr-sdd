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


@register.filter(name="highlight_mobile", is_safe=True)
def highlight_mobile(text, query):
    if not query or not text:
        return text
    text_str = str(text)
    clean_text = re.sub(r"[^0-9]", "", text_str)
    clean_query = re.sub(r"[^0-9]", "", query)
    if not clean_query or not clean_text:
        return text
    escaped = re.escape(clean_query)
    match = re.search(escaped, clean_text, re.IGNORECASE)
    if not match:
        return text
    match_start = match.start()
    match_end = match.end()
    result_parts = []
    digit_idx = 0
    marking = False
    for char in text_str:
        if char.isdigit():
            if digit_idx == match_start:
                result_parts.append("<mark>")
                marking = True
            result_parts.append(char)
            digit_idx += 1
            if digit_idx == match_end and marking:
                result_parts.append("</mark>")
                marking = False
        else:
            result_parts.append(char)
    if marking:
        result_parts.append("</mark>")
    return mark_safe("".join(result_parts))
