# Quickstart: Current Month Payments Report

## Implementation Steps

### Step 1: Modify `PaymentReportView.get_context_data()`

In `backend/apps/payments/views.py`, add defaults for `start` and `end` inside `get_context_data()`:

```python
from datetime import date
import calendar

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    grouping = self.request.GET.get("grouping", "month")
    start = self.request.GET.get("start", "")
    end = self.request.GET.get("end", "")
    today = date.today()
    if not start:
        start = today.replace(day=1).isoformat()
    if not end:
        _, last_day = calendar.monthrange(today.year, today.month)
        end = today.replace(day=last_day).isoformat()
    # ... rest of existing logic unchanged
```

### Step 2: Update tests

Add tests in `backend/tests/test_payments.py`:

1. `test_report_defaults_to_current_month` — no query params → dates are current month boundaries
2. `test_report_uses_provided_dates` — explicit dates override defaults
3. `test_report_current_month_no_payments` — empty state shown

### Step 3: Verify i18n

No new user-facing strings are introduced (existing labels and text are reused).

### Step 4: Verify all tests pass

```bash
docker compose exec web uv run pytest tests/test_payments.py -v
```
