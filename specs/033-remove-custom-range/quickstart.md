# Quickstart: Remove Custom Range

## What needs to change

Four files:

### 1. Template — remove dropdown option

**File**: `backend/apps/payments/templates/payments/payment_reports.html`

Remove the `<option>` for "Custom Range":

```html
<!-- Remove this line: -->
<option value="range" {% if grouping == "range" %}selected{% endif %}>{% translate "Custom Range" %}</option>
```

### 2. View — remove `range` branch

**File**: `backend/apps/payments/views.py`

Delete the entire `elif grouping == "range":` block (lines 229-232 in the current file):

```python
elif grouping == "range":
    rows = qs.values("date", "payment_type").annotate(
        total=Sum("amount"), count=Count("id"),
    ).order_by("date", "payment_type")
```

The default grouping in `get()` — `self.request.GET.get("grouping", "month")` — will gracefully handle any unrecognized `grouping` value, including `range`.

### 3. Tests — update range-related test

**File**: `backend/tests/test_payments.py`

Remove the `test_reports_day_grouping_with_date_range` test case if it specifically tests `grouping=range`. Update `test_reports_with_date_range` to no longer reference `range`.

### 4. i18n — remove translation entry

**File**: `backend/locale/es/LC_MESSAGES/django.po`

Remove these lines:

```
#: apps/payments/templates/payments/payment_reports.html:19
msgid "Custom Range"
msgstr "Rango personalizado"
```

Recompile: `docker compose exec web uv run manage.py compilemessages`

## Verify

1. Load Reports > Payments — confirm dropdown has only Day, Week, Month
2. Visit `/payments/reports/?grouping=range` — confirm page loads with month grouping (no error)
3. Date range inputs still work with Day/Week/Month groupings
4. Run `pytest -v -k "report"` — all 11 report tests pass (one removed)
