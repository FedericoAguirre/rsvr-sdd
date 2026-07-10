# Quickstart: Monthly Stacked Graph

## Step-by-Step

### Step 1 — Add date snapping in `PaymentReportView.get_context_data()`

In `backend/apps/payments/views.py`, after the existing week snapping block, add:

```python
elif grouping == "month" and start and end:
    try:
        import calendar
        start_dt = date.fromisoformat(start)
        end_dt = date.fromisoformat(end)
        start_dt = start_dt.replace(day=1)
        _, last_day = calendar.monthrange(end_dt.year, end_dt.month)
        end_dt = end_dt.replace(day=last_day)
        start = start_dt.isoformat()
        end = end_dt.isoformat()
    except (ValueError, TypeError):
        pass
```

### Step 2 — Update label format in `payment_reports.html`

In the `formatLabel()` function, update the fallback for monthly data:

```javascript
function formatLabel(r) {
    var raw = r.date || r.week || (r.date__year + '' + String(r.date__month).padStart(2, '0'));
    if (r.week) return raw.replace(/-/g, '');
    return raw;
}
```

The monthly case already returns `r.date__year + '' + String(r.date__month).padStart(2, '0')` — no change needed if it's already YYYYMM format (no `-` separator).

**Note**: The `date__year` + `date__month` concatenation in the existing code at line 65 produces `YYYYMM` already (the week case strips hyphens). Verify the current format matches the spec — if it currently contains a separator, remove it.

### Step 3 — Write tests

Add to `backend/tests/test_payments.py`:

```python
@patch("apps.payments.views.PaymentReportView.template_name", "payments/payment_reports.html")
class PaymentMonthlyReportTest(TestCase):
    def test_start_date_snaps_to_first_of_month(self):
        """Start date 2026-07-15 snaps to 2026-07-01."""
        ...

    def test_end_date_snaps_to_last_day_of_month(self):
        """End date 2026-09-10 snaps to 2026-09-30."""
        ...

    def test_start_date_already_first(self):
        """Start date already 1st — no adjustment."""
        ...

    def test_end_date_already_last_day(self):
        """End date already last day — no adjustment."""
        ...

    def test_leap_year_february(self):
        """February in leap year snaps to 29th."""
        ...

    def test_monthly_chart_renders(self):
        """Weekly chart rendering works with labels in YYYYMM format."""
        ...
```

### Step 4 — Verify

```bash
docker compose exec web uv run manage.py test
```
