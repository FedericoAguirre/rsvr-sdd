# Feature Specification: Monthly Stacked Graph

**Feature Branch**: `035-monthly-stacked-graph`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "using the @specs/034-stacked-graph-weekly-grouping/spec.md create the same functionality for grouping monthly, the stacked bar must be labeled as YYYYMM, the Start date must be pointed at the 1st day of that month, the End date must be pointed at the end day of that month."

## Clarifications

*No clarifications needed — behavior is directly adapted from the established weekly grouping spec (034).*

## User Scenarios & Testing

### User Story 1 — View monthly stacked payment chart with calendar month boundaries (P1)

An administrator navigates to Reports > Payments, selects "Month" grouping, and sees a stacked bar chart where each bar represents a calendar month. The start date automatically snaps to the 1st of that month, and the end date snaps to the last day of that month. Bars are labeled with the year and month in YYYYMM format (e.g., 202607).

**Why this priority**: This is the core feature — monthly grouping with correct month boundaries is the primary deliverable.

**Independent Test**: Load Reports > Payments with Month grouping and dates e.g. start=2026-07-15 and end=2026-09-10. Confirm the chart shows bars starting from 2026-07-01 and ending at 2026-09-30, labeled as 202607, 202608, 202609.

**Acceptance Scenarios**:

1. **Given** the administrator selects Month grouping with Start date 2026-07-15, **When** the chart renders, **Then** the first bar represents the month starting 2026-07-01, because the start date snapped backwards to the 1st of that month.
2. **Given** the administrator selects Month grouping with End date 2026-09-10, **When** the chart renders, **Then** the last bar represents the month ending 2026-09-30, because the end date snapped forwards to the last day of that month.
3. **Given** a Start date that is already the 1st of a month, **When** the chart renders, **Then** that date is used as-is without adjustment.
4. **Given** an End date that is already the last day of a month, **When** the chart renders, **Then** that date is used as-is without adjustment.
5. **Given** there are no payments for a particular month, **When** the chart renders, **Then** that month is omitted from the x-axis rather than showing an empty bar.
6. **Given** the chart is loaded with Month grouping, **When** the user hovers over any segment, **Then** a tooltip shows the payment type, total amount, and count for that month and type.

---

### User Story 2 — Stacked columns show totals on top (P2)

An administrator sees the total payment amount displayed on top of each stacked bar for quick visual reference.

**Why this priority**: Displaying totals on bars provides immediate insight without requiring tooltip interaction.

**Independent Test**: Visually confirm that each stacked bar has the total amount displayed above it.

**Acceptance Scenarios**:

1. **Given** a stacked bar chart with Month grouping, **When** the chart renders, **Then** each stacked bar has the total amount displayed on top of it.

---

### User Story 3 — Chart is responsive with grid lines (P3)

An administrator views the chart on different screen sizes and sees a responsive chart with Y-axis divisory lines and no horizontal scrolling.

**Why this priority**: Readability and responsiveness ensure the chart is useful on all devices.

**Independent Test**: Resize the browser window and confirm the chart resizes proportionally without clipping or horizontal scrolling.

**Acceptance Scenarios**:

1. **Given** the chart is displayed, **When** the user resizes the browser to a smaller viewport, **Then** the chart scales proportionally without horizontal scrolling.
2. **Given** the chart is displayed, **Then** the Y-axis shows horizontal divisory lines for readability.

### Edge Cases

- What if the start and end dates fall within the same calendar month? The chart should show a single bar for that month.
- What if the selected date range results in zero months after adjustment? Show the empty state message "No payment data for the selected period."
- What if payments exist only on a single day of a month? They are still included in the monthly bar for that calendar month.
- What if the backend aggregation query fails? Show a distinct error message in the chart area (e.g., "Failed to load chart data.").

## Requirements

### Functional Requirements

- **FR-001**: System MUST render a stacked bar chart for Month grouping where each bar represents a calendar month with segments per payment type.
- **FR-002**: The Start date MUST snap backwards to the 1st of that calendar month (same day if already the 1st). The date input field MUST update to display the snapped date.
- **FR-003**: The End date MUST snap forwards to the last day of that calendar month (same day if already the last day). The date input field MUST update to display the snapped date.
- **FR-004**: X-axis labels MUST display the year and month in YYYYMM format (e.g., 202607 for July 2026).
- **FR-005**: Empty months (no payment data) MUST be omitted from the x-axis.
- **FR-006**: Total amount MUST be displayed on top of each stacked bar.
- **FR-007**: Tooltips MUST show payment type, total amount, and count on hover.
- **FR-008**: The chart MUST be responsive and scale to fit the viewport width without horizontal scrolling.
- **FR-009**: The Y-axis MUST display horizontal divisory lines.

### Key Entities

- **Payment**: Contains `date`, `amount`, and `payment_type` fields. The `date` field determines which calendar month a payment belongs to.
- **Payment Report View**: Must adjust user-provided start/end dates to month boundaries (1st / last day) before passing to the aggregation query.

### Out of Scope

- Drill-down interaction (clicking a monthly bar → daily or weekly view)
- Data export (CSV/PDF)
- Chart animations and transitions
- Print styling / print-specific layout
- Caching or offline support
- Role-based access control beyond existing auth

## Success Criteria

### Measurable Outcomes

- **SC-001**: Administrators can view payment data grouped by calendar month with correct 1st-to-last-day boundaries.
- **SC-002**: Start date snapping (to 1st) and end date snapping (to last day) work correctly for any day of any month (verified with test cases across different months including February leap years).
- **SC-003**: All existing report tests pass after adding monthly grouping updates.
- **SC-004**: Chart renders without errors or visual clipping on viewports from 320px to 1920px wide.

## Assumptions

- The existing monthly aggregation (`date_trunc('month', date)`) in PostgreSQL returns calendar months starting on the 1st — compatible with this feature's requirements.
- The date snapping logic will be implemented in the backend (`PaymentReportView`) before passing dates to the query.
- The existing Chart.js stacked bar implementation from the weekly grouping feature will be reused and adapted for monthly grouping.
- User-facing strings (labels, tooltips) will reuse existing i18n keys where possible; new keys will follow the i18n convention.
