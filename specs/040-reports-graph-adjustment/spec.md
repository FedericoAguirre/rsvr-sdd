# Feature Specification: Reports Graph Adjustment

**Feature Branch**: `040-reports-graph-adjustment`

**Created**: 2026-07-13

**Status**: Draft

**Input**: User description: "As system user I want to see the graph in the payments/reports page adjusted, so I don't need to scroll down to see it complete."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full Chart Visibility (Priority: P1)

When a system user navigates to the payments reports page, the chart container height is set so the entire chart is visible in the viewport without requiring vertical scrolling.

**Why this priority**: This is a pure UX improvement — users should see the complete chart at a glance without extra scrolling.

**Independent Test**: Can be fully tested by loading the payments reports page and verifying that the chart canvas and its entire content fit within the visible area without scrolling the page.

**Acceptance Scenarios**:

1. **Given** I am on the payments reports page with chart data rendered, **When** the page loads, **Then** the entire chart (including bar labels and totals) is visible without vertical scrolling.
2. **Given** I am on the payments reports page with no chart data (empty state), **When** the page loads, **Then** the empty state message is visible without excessive whitespace.

---

### Edge Cases

- What if the chart has many data points that make bars too small? The height should accommodate at least 31 daily bars (one month) without clipping.
- What if the viewport is very small (e.g., 768px wide tablet)? The chart should still be fully visible, potentially with reduced height.
- What if the user has set a custom browser zoom level? The chart container should scale gracefully.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chart container on the payments reports page MUST have a CSS height that ensures all chart content (bars, labels, totals) is visible without page scrolling.
- **FR-002**: The chart canvas MUST maintain aspect ratio so bars and labels are not distorted.
- **FR-003**: The empty state message area MUST NOT have excessive whitespace — it should fit within a compact container.
- **FR-004**: The chart height MUST be responsive — it should work on viewports at least 768px wide.

### Key Entities *(include if feature involves data)*

No new entities — this is a purely presentational/CSS change to the existing reports template.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users see the complete chart on page load without scrolling.
- **SC-002**: Chart bars, labels, and totals are fully readable without distortion.
- **SC-003**: No regression in existing chart rendering — data still displays correctly after height adjustment.
- **SC-004**: The page layout remains balanced — no excessive whitespace below the chart.

## Assumptions

- The existing chart is rendered via Chart.js in a `<canvas>` element inside a card container.
- The chart currently requires scrolling because the default container height is too large (e.g., 400px).
- "Visible without scrolling" means the chart fits within the initial viewport (above the fold) for a typical desktop screen (1080p+).
- CSS-only changes to the container's `height` or `max-height` property (or the canvas `aspect-ratio`) are sufficient — no JavaScript resize logic needed.
- The chart auto-resizes to fit its container when the container dimensions change.
- No changes to the graph data, colors, or rendering logic — only container sizing.
