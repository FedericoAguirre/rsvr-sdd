# Feature Specification: Stacked Graph Weekly Grouping

**Feature Branch**: `034-stacked-graph-weekly-grouping`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "From ai/features/todos/06-1-stacked-graph-weekly-grouping.md create the specs for the new feature"

## Clarifications

### Session 2026-07-10

- Q: Should empty weeks be omitted or shown as zero-height bars? → A: Omit empty weeks from the x-axis (FR-005 unchanged).
- Q: How to handle backend aggregation errors? → A: Show a distinct error message in the chart area.
- Q: What is explicitly out of scope? → A: Drill-down (click week → daily), data export (CSV/PDF), chart animations, and print styling.
- Q: Should the chart include accessibility accommodations for screen readers? → A: No a11y accommodations needed (chart is purely visual).
- Q: Should date inputs update to reflect snapped Monday/Sunday boundaries? → A: Yes, date input fields update to show snapped values.

## User Scenarios & Testing

### User Story 1 — View weekly stacked payment chart with ISO week boundaries (P1)

An administrator navigates to Reports > Payments, selects "Week" grouping, and sees a stacked bar chart where each bar represents an ISO week. The start date automatically snaps to the closest previous Monday, and the end date snaps to the closest next Sunday. Bars are labeled with the Monday date in YYYYMMDD format.

**Why this priority**: This is the core feature — weekly grouping with correct ISO week boundaries is the primary deliverable.

**Independent Test**: Load Reports > Payments with Week grouping and dates e.g. start=2026-07-03 (Friday) and end=2026-07-19 (Sunday). Confirm the chart shows bars starting from Monday 2026-07-06 and ending at Sunday 2026-07-19, labeled with Monday dates.

**Acceptance Scenarios**:

1. **Given** the administrator selects Week grouping with Start date 2026-07-03 (Friday), **When** the chart renders, **Then** the first bar represents the week starting Monday 2026-07-06, because the start date snapped backwards to the closest Monday.
2. **Given** the administrator selects Week grouping with End date 2026-07-19 (Sunday), **When** the chart renders, **Then** the last bar represents the week ending Sunday 2026-07-19, because the end date snapped forwards to the closest Sunday.
3. **Given** a Start date that is already a Monday, **When** the chart renders, **Then** that Monday is used as-is without adjustment.
4. **Given** an End date that is already a Sunday, **When** the chart renders, **Then** that Sunday is used as-is without adjustment.
5. **Given** there are no payments for a particular week, **When** the chart renders, **Then** that week is omitted from the x-axis rather than showing an empty bar.
6. **Given** the chart is loaded with Week grouping, **When** the user hovers over any segment, **Then** a tooltip shows the payment type, total amount, and count for that week and type.

---

### User Story 2 — Stacked columns show totals on top (P2)

An administrator sees the total payment amount displayed on top of each stacked bar for quick visual reference.

**Why this priority**: Displaying totals on bars provides immediate insight without requiring tooltip interaction.

**Independent Test**: Visually confirm that each stacked bar has the total amount displayed above it.

**Acceptance Scenarios**:

1. **Given** a stacked bar chart with Week grouping, **When** the chart renders, **Then** each stacked bar has the total amount displayed on top of it.

---

### User Story 3 — Chart is responsive with grid lines (P3)

An administrator views the chart on different screen sizes and sees a responsive chart with Y-axis divisory lines and no horizontal scrolling.

**Why this priority**: Readability and responsiveness ensure the chart is useful on all devices.

**Independent Test**: Resize the browser window and confirm the chart resizes proportionally without clipping or horizontal scrolling.

**Acceptance Scenarios**:

1. **Given** the chart is displayed, **When** the user resizes the browser to a smaller viewport, **Then** the chart scales proportionally without horizontal scrolling.
2. **Given** the chart is displayed, **Then** the Y-axis shows horizontal divisory lines for readability.

### Edge Cases

- What if the start and end dates fall within the same ISO week? The chart should show a single bar for that week.
- What if the selected date range results in zero weeks after adjustment? Show the empty state message "No payment data for the selected period."
- What if payments exist only on weekends? They are still included in the weekly bar for the ISO week they fall in.
- What if the backend aggregation query fails? Show a distinct error message in the chart area (e.g., "Failed to load chart data.").

## Requirements

### Functional Requirements

- **FR-001**: System MUST render a stacked bar chart for Week grouping where each bar represents an ISO week (Monday–Sunday) with segments per payment type.
- **FR-002**: The Start date MUST snap backwards to the closest preceding Monday (same day if already Monday). The date input field MUST update to display the snapped date.
- **FR-003**: The End date MUST snap forwards to the closest following Sunday (same day if already Sunday). The date input field MUST update to display the snapped date.
- **FR-004**: X-axis labels MUST display the Monday date of each ISO week in YYYYMMDD format.
- **FR-005**: Empty weeks (no payment data) MUST be omitted from the x-axis.
- **FR-006**: Total amount MUST be displayed on top of each stacked bar.
- **FR-007**: Tooltips MUST show payment type, total amount, and count on hover.
- **FR-008**: The chart MUST be responsive and scale to fit the viewport width without horizontal scrolling.
- **FR-009**: The Y-axis MUST display horizontal divisory lines.

### Key Entities

- **Payment**: Contains `date`, `amount`, and `payment_type` fields. The `date` field determines which ISO week a payment belongs to.
- **Payment Report View**: Must adjust user-provided start/end dates to ISO week boundaries before passing to the aggregation query.

### Out of Scope

- Drill-down interaction (clicking a weekly bar → daily view)
- Data export (CSV/PDF)
- Chart animations and transitions
- Print styling / print-specific layout
- Caching or offline support
- Role-based access control beyond existing auth

## Success Criteria

### Measurable Outcomes

- **SC-001**: Administrators can view payment data grouped by ISO week with correct Monday–Sunday boundaries.
- **SC-002**: Start date snapping and end date snapping work correctly for any day of the week (verified with test cases for each weekday).
- **SC-003**: All existing report tests pass after adding weekly grouping updates.
- **SC-004**: Chart renders without errors or visual clipping on viewports from 320px to 1920px wide.

## Assumptions

- The existing weekly grouping (`date_trunc('week', date)`) in PostgreSQL returns ISO weeks starting on Monday — compatible with this feature's requirements.
- The date snapping logic will be implemented in the backend (`PaymentReportView`) before passing dates to the query.
- The existing Chart.js stacked bar implementation from the daily grouping feature will be reused and adapted for weekly grouping.
- User-facing strings (labels, tooltips) will reuse existing i18n keys where possible; new keys will follow the i18n convention.
