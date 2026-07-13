# Research: Reports Graph Adjustment

## Existing Template Structure

**File**: `backend/apps/payments/templates/payments/payment_reports.html`

### Current Chart Container (lines 42-53)

```html
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5>{% translate "Totals by Payment Type" %}</h5>
            </div>
            <div class="card-body">
                <canvas id="totalsChart" width="400" height="300"></canvas>
            </div>
        </div>
    </div>
</div>
```

### Current Issues

- Chart.js renders at 400×300px (hardcoded canvas attributes)
- No max-height or overflow control on `.card-body`
- Chart can exceed viewport height when many data points are displayed (especially with daily grouping and stacked bars + total labels)

### Approach Decision

**Strategy**: CSS-only adjustment — add a `max-height` with `overflow-y: auto` to the `.card-body` containing the canvas, and set the canvas to a responsive height via CSS.

- The canvas `width`/`height` attributes will remain for initial render
- CSS will override with `max-height: 300px` (or similar) and `width: 100%`
- Chart.js `options.responsive = true` will handle resize

## Edge Cases

| Case | Resolution |
|------|-----------|
| Many data points (31 daily bars) | Scroll within card body if needed, but ideally container fits viewport |
| Empty state (no data) | Compact height — no excessive whitespace |
| Small viewport (<768px) | Chart stacks vertically; height still manageable |
