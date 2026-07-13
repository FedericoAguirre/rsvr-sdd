# Contract: Payment Reports View — Chart Container

## Component

- **Location**: `backend/apps/payments/templates/payments/payment_reports.html`
- **Selector**: `#totalsChart` canvas inside `.card-body`
- **Library**: Chart.js (bar chart, stacked)

## Current Behavior

- Canvas renders at fixed 400×300px (hardcoded `width`/`height` attributes)
- `.card-body` has no height constraints
- Chart may overflow viewport on short screens

## Target Behavior

- Chart container height limited so full chart (bars, labels, totals) is visible without page scrolling
- `.card-body` has `max-height: 350px` with `overflow-y: auto` for graceful fallback on dense data
- Canvas `height` attribute adjusted to `250` for a more compact default
- Chart.js `responsive: true` handles canvas resize to container
