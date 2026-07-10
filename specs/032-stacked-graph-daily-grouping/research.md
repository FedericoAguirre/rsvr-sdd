# Research: Stacked Graph Daily Grouping

## Research Tasks

1. **Chart.js stacked bar chart configuration** — understand the API for stacked bars
2. **Data transformation** — convert backend time-grouped data into Chart.js stacked datasets
3. **Color palette** — consistent payment type colors across the chart

---

## Decision 1: Chart.js Stacked Bar Configuration

**Decision**: Use Chart.js `type: 'bar'` with `options.scales.x.stacked: true` and `options.scales.y.stacked: true`.

**Rationale**:
- Chart.js v4 supports stacked bars natively without plugins.
- Each payment type becomes a separate dataset with `data` array aligned to time period labels.
- The `stacked: true` option on both axes ensures segments stack vertically.

**Implementation pattern**:
```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['2026-07-01', '2026-07-02', ...],  // time periods
    datasets: [{
      label: 'CASH',
      data: [150.00, 200.00, ...],
      backgroundColor: 'rgba(54, 162, 235, 0.7)',
    }, {
      label: 'CC',
      data: [300.00, 100.00, ...],
      backgroundColor: 'rgba(255, 99, 132, 0.7)',
    }, ...]
  },
  options: {
    scales: {
      x: { stacked: true },
      y: { stacked: true, beginAtZero: true }
    },
    plugins: {
      legend: { display: true, onClick: /* toggle dataset */ },
      tooltip: { /* period, type, amount */ }
    }
  }
});
```

**Alternatives considered**:
- **Chart.js `type: 'stackedBar'`**: No such type — stacking is an option on `bar`, not a separate chart type.
- **ECharts**: Would require adding a new library dependency — rejected per constraints.

---

## Decision 2: Data Transformation

**Decision**: Transform the backend JSON on the client side from a flat row list into a time-indexed datasets structure.

**Rationale**:
- Backend returns rows like `[{date: "2026-07-01", payment_type: "CASH", total: 150.00}, ...]`
- Chart.js needs datasets keyed by payment_type with arrays indexed by time period.
- Client-side JS process:
  1. Collect all unique time period labels (e.g., dates) maintaining chronological order
  2. Collect all unique payment types
  3. For each payment type, build an array of totals aligned to the label order
  4. Create one dataset per payment type with its color and data array

**Alternatives considered**:
- **Backend restructuring**: Could reshape the JSON on the server, but this would change the `PaymentReportView` and its test expectations — rejected to minimize changes.

---

## Decision 3: Color Palette

**Decision**: Use the existing 5-color palette from the current chart, mapped consistently to payment types.

**Rationale**:
- The current chart already defines 5 colors — reuse them to maintain visual consistency.
- Payment types are: CASH, CC, DC, TRANSF, PAPP — 5 types, 5 colors.

**Color mapping**:
| Payment Type | Color |
|-------------|-------|
| CASH | `rgba(54, 162, 235, 0.7)` (blue) |
| CC | `rgba(255, 99, 132, 0.7)` (red) |
| DC | `rgba(255, 206, 86, 0.7)` (yellow) |
| TRANSF | `rgba(75, 192, 192, 0.7)` (green) |
| PAPP | `rgba(153, 102, 255, 0.7)` (purple) |

**Alternatives considered**:
- **Auto-generated palette**: Not needed — 5 static colors are sufficient and match existing UI.
