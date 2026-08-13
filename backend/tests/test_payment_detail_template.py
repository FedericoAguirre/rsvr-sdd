from pathlib import Path

TEMPLATE = (
    Path(__file__).parents[1]
    / "apps/payments/templates/payments/payment_detail.html"
)


def test_batch_date_grid_groups_dates_by_calendar_week_and_weekday():
    source = TEMPLATE.read_text()

    assert "var weekStart = addDays" in source
    assert "weekGroups[weekStart][pyDow]" in source
    assert "for (var column = 0; column < 5; column++)" in source


def test_batch_date_buttons_keep_exact_iso_dates():
    source = TEMPLATE.read_text()

    assert 'data-date="\' + cell.date + \'"' in source
    assert 'data-dow="\' + cell.dow + \'"' in source


def test_batch_date_grid_preserves_translated_weekday_headers_and_reserved_filtering():
    source = TEMPLATE.read_text()

    assert "DAY_ABBRS[column]" in source
    assert "reservedSet[d]" in source


def test_payment_receipt_actions_are_adjacent_to_calendar_download():
    source = TEMPLATE.read_text()

    receipt_idx = source.find('{% translate "Download payment" %}')
    calendar_idx = source.find('{% translate "Download calendar" %}')
    assert receipt_idx != -1
    assert calendar_idx != -1
    assert receipt_idx < calendar_idx
    assert 'data-pdf-url="{% url \'receipt\' payment.pk %}"' in source
    assert "{% url 'payments:calendar' payment.pk %}" in source


def test_payment_receipt_ui_contains_loading_and_clipboard_fallback_hooks():
    source = TEMPLATE.read_text()

    assert "receiptLoading" in source
    assert "navigator.clipboard" in source
    assert "receiptFallback" in source
    assert "receiptError" in source
