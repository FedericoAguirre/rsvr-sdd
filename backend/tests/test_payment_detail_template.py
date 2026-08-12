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
