# Quickstart: Remove Distribution Graph

## Implementation Steps

1. Open `backend/apps/payments/templates/payments/payment_reports.html`
2. **Remove the Distribution card column** — delete lines 48-57 (the second `col-md-6` div containing the Distribution card with `id="distributionChart"` canvas)
3. **Widen the Totals column** — change `col-md-6` to `col-12` on line 38
4. **Remove the pie chart JS** — delete lines 107-122 (the JavaScript block that instantiates `distributionChart`)
5. **Verify**: Load the payments/reports/ page; confirm only the bar chart appears; check browser console for no JS errors

## Verification

```bash
cd backend
python manage.py runserver
# Visit /payments/reports/ — only one chart should render
```
