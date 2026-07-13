# Feature Specification: Current Month Payments Report

**Feature Branch**: `001-current-month-report`

**Created**: 2026-07-13

**Status**: Draft

**Input**: User description: "As system user I want to get the payments reports grouped by date during the current month, so i can quickly spot the earnings. Another goal is to have the input fields preselected with the proper values to query the report"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Current Month Auto-Preselection (Priority: P1)

When a system user navigates to the payments reports page, the date range inputs are automatically pre-filled with the first and last day of the current month, so they do not need to manually enter dates.

**Why this priority**: This is the core usability improvement — users save time and avoid date-entry errors every time they visit the reports page.

**Independent Test**: Can be fully tested by loading the payments reports page and verifying that the start/end date fields contain the first and last day of the current month.

**Acceptance Scenarios**:

1. **Given** I am on the payments reports page, **When** the page loads, **Then** the start date field contains the first day of the current month (e.g., `2026-07-01` for July 2026).
2. **Given** I am on the payments reports page, **When** the page loads, **Then** the end date field contains the last day of the current month (e.g., `2026-07-31` for July 2026).
3. **Given** I am on the payments reports page, **When** the page loads for the first time in a new month, **Then** the date fields reflect the new month, not the previous one.

---

### User Story 2 - Auto-Render with Current Month Data (Priority: P1)

Once the page loads with current month defaults, the earnings report (grouped by date) and the graph are automatically rendered without requiring the user to click a search or generate button.

**Why this priority**: The whole point of pre-filling dates is to eliminate extra steps — the report must render immediately for the feature to deliver value.

**Independent Test**: Can be fully tested by loading the payments reports page and verifying that the earnings data and graph are displayed without any additional user action.

**Acceptance Scenarios**:

1. **Given** I am on the payments reports page with current month pre-filled, **When** the page finishes loading, **Then** the payments table or list shows entries grouped by date for the current month.
2. **Given** I am on the payments reports page with current month pre-filled, **When** the page finishes loading, **Then** the earnings graph is automatically rendered.
3. **Given** the current month has no payments, **When** the page loads, **Then** an appropriate message is displayed indicating no data for the period (instead of an empty/error state).

---

### User Story 3 - Manual Date Override (Priority: P2)

After the page loads with current month defaults, the user can modify the start/end date fields and re-query the report for a different period.

**Why this priority**: Users still need the flexibility to view reports for other periods, but this is secondary to the default behavior.

**Independent Test**: Can be fully tested by changing the date fields to a different month and confirming the report and graph update accordingly.

**Acceptance Scenarios**:

1. **Given** the report is displayed with current month data, **When** I change the start date to a previous month and trigger the query, **Then** the report updates to show data for the new date range.
2. **Given** I have changed the date fields, **When** I navigate away and return, **Then** the fields reset to the current month defaults (not the previously selected range).

---

### Edge Cases

- What happens if the user's system clock is in a different timezone? The month boundaries should be determined server-side to avoid timezone discrepancies.
- How does the system behave when the current month has no payment data at all? The page should show an empty state message rather than an error or blank screen.
- What happens on the last day of the month at 23:59? The end date should still correctly be that day — no off-by-one errors.
- If the user clears the date fields and submits, should the system fall back to current month defaults or show an error? Reasonable default: re-apply current month defaults.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST pre-fill the start date input with the first day of the current month when the payments reports page loads.
- **FR-002**: System MUST pre-fill the end date input with the last day of the current month when the payments reports page loads.
- **FR-003**: System MUST automatically trigger the report query on page load when date fields are pre-filled with defaults (no extra user action required).
- **FR-004**: System MUST display payments grouped by calendar date with daily earnings totals for the selected date range.
- **FR-005**: System MUST allow the user to modify the start and/or end date after page load and re-query the report.
- **FR-006**: System MUST display total earnings (sum of all payments) for the selected date range alongside the daily breakdown.
- **FR-007**: System MUST handle the empty-data case gracefully — display a clear message when no payments exist for the selected range.
- **FR-008**: System MUST reset date fields to current month defaults when the user navigates away and returns to the page.

### Key Entities *(include if feature involves data)*

- **Payment**: An individual financial transaction record with an amount, date, and associated metadata (client, concept, payment type).
- **Daily Earnings Aggregate**: A grouping of payments by calendar date, summing amounts per day to show daily revenue.
- **Report Query**: The combination of start date and end date parameters used to filter and generate the payments report.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users see the current month's date range pre-filled on every visit to the payments reports page without any manual entry.
- **SC-002**: The earnings report and graph render automatically on page load without requiring a button click or additional action.
- **SC-003**: Daily grouped earnings are displayed in a clear, scannable format (table or list) ordered by date.
- **SC-004**: Users can modify the date range and see updated results in under 2 seconds (existing performance baseline).
- **SC-005**: Zero regression in existing reports functionality — all existing date-range queries continue to work.

## Assumptions

- An existing payments reports page with date range inputs and a graph already exists and works correctly.
- The "graph" mentioned in the user story refers to the existing earnings graph component (not a new visualization).
- "Grouped by date" means daily aggregation — each calendar date shows the sum of all payments on that day.
- "Earnings" means the total monetary amount of payments (sum of payment amounts), not a net-profit calculation.
- The current month is determined server-side to avoid client/server timezone mismatches.
- Date format follows the project's existing convention (YYYY-MM-DD or locale-specific as already used on the reports page).
- No new database columns or tables are required — only changes to the existing report query/view logic.
- Custom date ranges (months other than the current one) remain fully functional after this change.
