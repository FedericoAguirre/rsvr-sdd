# Feature Specification: Remove Distribution Graph

**Feature Branch**: `025-remove-distribucion-graph`

**Created**: 2026-06-24

**Status**: Draft

**Input**: User description: "I want to delete the Distribución graph from the payments/reports/ webpage"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admin views cleaner payment reports page (Priority: P1)

An administrator visits the payments/reports/ page and sees only the relevant bar chart showing totals by payment type, without the redundant Distribution pie chart that shows the same data in a different format.

**Why this priority**: This is the only requirement — removing the duplicate visualization. The page loads faster and presents a cleaner, more focused view.

**Independent Test**: Can be fully tested by navigating to the reports page and confirming only one chart (the bar chart) is visible. Delivers a cleaner reporting interface.

**Acceptance Scenarios**:

1. **Given** the administrator is on the payments/reports/ page, **When** the page loads, **Then** only the "Totals by Payment Type" bar chart is displayed
2. **Given** the administrator views the reports page, **When** they inspect the page content, **Then** no Distribution pie chart is present
3. **Given** the removal of the Distribution chart, **When** the page loads, **Then** the layout properly fills the available space without broken elements

---

### Edge Cases

- What happens if JavaScript fails to render the remaining Totals chart? The page should still be usable — the chart canvas will simply not display, but no errors should break other page functionality
- What if the report data is empty? The page should show no charts, not error out, and display appropriate empty-state messaging

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The payments/reports/ page MUST no longer display the Distribution pie chart
- **FR-002**: All other page content — including the Totals by Payment Type bar chart, report filters, and form controls — MUST remain intact and functional
- **FR-003**: The page layout MUST gracefully fill the space left by the removed chart (no broken columns, empty card containers, or layout shifts)
- **FR-004**: Removing the Distribution chart MUST NOT introduce any JavaScript errors or break the rendering of the remaining Totals chart

### Key Entities *(include if feature involves data)*

No new data entities are introduced. This feature only modifies the presentation of the existing reports page — the underlying report data and its generation remain unchanged.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The Distribution pie chart is no longer visible on the payments/reports/ page when accessed by an administrator
- **SC-002**: The Totals by Payment Type bar chart continues to render and function correctly with the same data as before
- **SC-003**: The page loads without any JavaScript console errors related to chart rendering
- **SC-004**: The page layout adjusts cleanly to fill the space previously occupied by the removed chart (no empty card frames or layout gaps)

## Assumptions

- The Distribution chart displays data already shown by the Totals by Payment Type bar chart, making it redundant
- No user has specifically requested or relies on the Distribution chart for their workflow
- The bar chart alone provides sufficient information about payment type distribution
- No changes to the backend report data generation are required — this is purely a presentation change
