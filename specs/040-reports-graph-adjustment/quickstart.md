# Quickstart: Reports Graph Adjustment

## Implementation Steps

### Step 1: Adjust template canvas and container sizing

In `backend/apps/payments/templates/payments/payment_reports.html`:

1. Change canvas `height` from `300` to `250`
2. Add `style="max-height: 350px; overflow-y: auto;"` to the `.card-body` div

### Step 2: Update tests

Add a test in `backend/tests/test_payments.py` to verify the canvas container has the correct height attribute.

### Step 3: Verify no regression

```bash
docker compose exec web uv run pytest tests/test_payments.py -v
```
