# Feature Specification: Stacked Graph Daily Grouping

**Feature Branch**: `032-stacked-graph-daily-grouping`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "Create the stacked graph for daily grouping"

## User Scenarios & Testing

### User Story 1 — View daily stacked payment chart (P1)

An administrator navigates to Reports > Payments and sees a stacked bar chart where each bar represents a day and segments within the bar show the breakdown by payment type (cash, credit card, debit card, transfer, app payment). The chart replaces the existing flat bar chart that only showed totals per payment type without the time dimension.

**Why this priority**: This is the core feature — transforming the existing chart into a meaningful time-series visualization. Without this, the feature delivers no value.

**Independent Test**: Can be fully tested by loading the Reports > Payments page with the default grouping and visually confirming the chart renders as a stacked bar chart with daily bars and payment type segments.

**Acceptance Scenarios**:

1. **Given** the user is on the Reports > Payments page with "Day" grouping selected, **When** the page loads, **Then** a stacked bar chart is displayed with one bar per day and segments colored by payment type.
2. **Given** there is no payment data for the selected period, **When** the page loads, **Then** a message is displayed indicating no data is available instead of an empty chart.
3. **Given** the user changes the grouping to "Week", **When** the page reloads, **Then** the chart updates to show one bar per week with payment type segments stacked.

---

### User Story 2 — Hover to see payment type breakdown (P2)

An administrator hovers over a segment of any stacked bar and sees a tooltip showing the date/week label, payment type name, and the exact total amount for that segment.

**Why this priority**: Tooltips provide drill-down detail without cluttering the chart. This is a usability improvement that makes the chart informative.

**Independent Test**: Can be tested by hovering any chart segment and verifying the tooltip appears with correct data.

**Acceptance Scenarios**:

1. **Given** a stacked bar chart is displayed, **When** the user hovers over any colored segment, **Then** a tooltip shows the date (or week/month label), payment type, and amount.
2. **Given** the chart has multiple segments in one bar, **When** the user hovers over different segments, **Then** each tooltip shows the correct corresponding data.

---

### User Story 3 — Toggle payment types on/off (P3)

An administrator clicks on a legend item (e.g., "Cash") and that payment type is hidden from the chart, allowing comparison of remaining types. Clicking again restores it.

**Why this priority**: Legend toggling is a standard chart interaction that lets users focus on specific payment types. It enhances data exploration without requiring backend changes.

**Independent Test**: Can be tested by clicking each legend item and verifying the corresponding segments disappear and reappear from the stacked bars.

**Acceptance Scenarios**:

1. **Given** a stacked bar chart with a legend, **When** the user clicks on a payment type in the legend, **Then** that type's segments are hidden from all bars and the legend item is dimmed.
2. **Given** a payment type is hidden, **When** the user clicks its dimmed legend item again, **Then** the segments reappear and the legend item is restored.

### Edge Cases

- What happens when all payment types are toggled off via the legend? The chart should show an empty state or a message indicating no data is displayed.
- How does the chart handle a day with only a single payment type? The bar should show a single full-height segment in that payment type's color.
- What if the backend returns zero total for a payment type on a given day? That payment type should not appear as a zero-height segment (no segment rendered).
- How does the chart behave with the "Custom Range" grouping? It should behave identically to "Day" grouping, showing bars for each date in the range.

## Requirements

### Functional Requirements

- **FR-001**: System MUST render a stacked bar chart on the Reports > Payments page showing time-grouped data (day/week/month/range) with one bar per time period.
- **FR-002**: Each bar MUST be segmented by payment type (CASH, CC, DC, TRANSF, PAPP), with segments sized proportionally to the total amount for that type on that period.
- **FR-003**: System MUST display a legend showing all available payment types with distinct colors.
- **FR-004**: Users MUST be able to toggle payment types on/off by clicking legend items, hiding or showing corresponding segments.
- **FR-005**: System MUST display tooltips on hover showing the period label, payment type name, and total amount.
- **FR-006**: System MUST show a "no data" message when there are no payments for the selected period, instead of an empty chart.
- **FR-007**: All groupings (day, week, month, custom range) MUST render as stacked bar charts. The "Custom Range" grouping uses daily bars within the selected range.

### Key Entities

- **Payment**: Contains `date`, `amount`, and `payment_type` fields. This is the source data for the chart. Each payment contributes to one segment of one bar based on its date and payment type.
- **Payment Report View**: The existing view that aggregates payments by time period and payment type. The backend already returns the correct data structure; only the frontend rendering needs to change.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Administrators can view daily/weekly/monthly payment totals broken down by payment type in a single stacked bar chart, replacing the current flat bar chart that lacks a time dimension.
- **SC-002**: Legend toggle and hover tooltip interactions respond within 100ms of user action (no perceivable delay).
- **SC-003**: The chart renders correctly in the latest versions of Chrome, Firefox, and Safari.
- **SC-004**: Zero regressions on existing report page functionality (filter form, grouping selector, date range inputs continue to work).

## Assumptions

- The existing Chart.js library (v4) loaded via CDN in `base.html` supports stacked bar charts and will be used for this feature.
- The existing `PaymentReportView` backend already returns the correct time-grouped data with `payment_type` breakdown — only the frontend chart rendering requires changes.
- The "Daily Grouping" name refers to the "Day" grouping mode in the existing reports page, but the same stacked chart approach applies to all grouping modes (day, week, month, custom range).
- Administrators are the sole audience for the reports page; regular users cannot access it.
- Colors for payment types will be assigned consistently: a fixed palette (as used currently) mapped to each payment type label.
