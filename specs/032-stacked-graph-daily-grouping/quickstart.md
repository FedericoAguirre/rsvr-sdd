# Quickstart: Stacked Graph Daily Grouping

## What needs to change

Single file: `backend/apps/payments/templates/payments/payment_reports.html`

Rewrite the `<script>` block (lines 52-98) that renders the Chart.js bar chart.

## How to implement

### 1. Data transformation

Replace the flat aggregation logic with a time-indexed datasets builder:

```javascript
// Group rows by time period
var labels = [...new Set(data.map(function(r) { return r.date || r.week || r.date__year + '-' + r.date__month; }))];
labels.sort();

// Get unique payment types
var types = [...new Set(data.map(function(r) { return r.payment_type; }))];

// Build datasets: one per payment type
var datasets = types.map(function(type, i) {
  return {
    label: type,
    data: labels.map(function(label) {
      var match = data.find(function(r) {
        return (r.date === label || r.week === label || (r.date__year && (r.date__year + '-' + r.date__month) === label)) && r.payment_type === type;
      });
      return match ? parseFloat(match.total) : 0;
    }),
    backgroundColor: colors[i]
  };
});
```

### 2. Chart options

Change chart type to `bar` with stacking enabled:

```javascript
options: {
  scales: {
    x: { stacked: true },
    y: { stacked: true, beginAtZero: true }
  },
  plugins: {
    legend: { display: true },
    tooltip: {
      callbacks: {
        label: function(ctx) { return ctx.dataset.label + ': $' + ctx.parsed.y; }
      }
    }
  }
}
```

### 3. Legend interaction

Remove `legend: { display: false }` — Chart.js v4 default legend click toggles datasets on/off. No custom code needed.

### 4. Empty state

Add a check before chart initialization:

```javascript
if (labels.length === 0 || types.length === 0) {
  // Show "no data" message in the card body
  document.querySelector('#totalsChart').insertAdjacentHTML('afterend', '<p>No payment data for the selected period.</p>');
  return;
}
```

## Test

```bash
docker compose exec web uv run manage.py test test_payments
```

## i18n

No new user-visible strings introduced. The existing `{% translate "Totals by Payment Type" %}` header and `{% translate "Total Amount" %}` label are reused. The empty state message needs i18n:

```html
{% translate "No payment data for the selected period." %}
```

## Verify

1. Navigate to Reports > Payments
2. Select "Day" grouping — confirm stacked bars by date
3. Select "Week" — confirm weekly stacked bars
4. Click legend items — confirm toggle
5. Hover segments — confirm tooltips
