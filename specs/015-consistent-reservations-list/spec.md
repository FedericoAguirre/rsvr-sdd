# Feature Specification: Consistent Reservations List

**Feature Branch**: `016-consistent-reservations-list`

**Created**: 2026-06-20

**Status**: Draft

**Input**: User description: "Use the same reservations list format"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View reservations with consistent fields (Priority: P1)

As an Operator, when I access the /reservations webpage, I want to see the same set of fields (Date, Client, Class Slot, Equipment, Status, View) regardless of whether I just loaded the page, applied a filter, or cleared a filter. This allows me to have a predictable and coherent experience when managing reservations.

**Why this priority**: This is the core fix — the inconsistency is the reported bug. All other scenarios depend on this behavior being correct.

**Independent Test**: Can be fully tested by navigating to the /reservations page and verifying all six fields/columns are visible in the list.

**Acceptance Scenarios**:

1. **Given** I am an Operator on the /reservations webpage, **When** the page first loads, **Then** the reservations list displays the following fields: Date, Client, Class Slot, Equipment, Status, and a View button.
2. **Given** I am an Operator viewing the /reservations webpage, **When** I apply any filter, **Then** the reservations list continues to display all six fields (Date, Client, Class Slot, Equipment, Status, View), with no fields removed.
3. **Given** I am an Operator viewing a filtered reservations list, **When** I clear the applied filter, **Then** the reservations list still displays all six fields (Date, Client, Class Slot, Equipment, Status, View), with no fields removed.

---

### User Story 2 - Export PDF remains unaffected (Priority: P2)

As an Operator, I want the Export PDF functionality to work exactly as it did before, so that the fix for the list display does not break my existing workflow.

**Why this priority**: The feature explicitly states Export PDF must not change. This protects existing functionality from regression.

**Independent Test**: Can be independently tested by exporting any reservation as PDF and verifying the output matches the previous format exactly.

**Acceptance Scenarios**:

1. **Given** I am an Operator viewing the /reservations webpage, **When** I export a reservation as PDF, **Then** the PDF output is identical in format and content to the previous behavior (no fields added, removed, or reordered).

---

### Edge Cases

- What happens when the reservations list is empty (no reservations match the current view or filter)? All six column headers should still be displayed, with an empty state message.
- How does the system handle rapid successive filter applications and clears? The list should display all six fields consistently across each state transition.
- What happens when a network error occurs during filter application? The list should either show the previous state with all six fields, or a meaningful error message — but should never revert to a partial column set.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The reservations list MUST display the following fields in this order: Date, Client, Class Slot, Equipment, Status, and a View button.
- **FR-002**: The set of displayed fields MUST remain unchanged after any filter operation (apply, modify, or clear).
- **FR-003**: The set of displayed fields MUST remain unchanged after the page is initially loaded.
- **FR-004**: The Export PDF functionality MUST produce the same output format as before this change, with no modifications to its content, layout, or behavior.

### Key Entities *(include if feature involves data)*

- **Reservation**: A booking record displayed in the list. Contains attributes: Date, Client name, Class Slot time/name, Equipment details, Status (e.g., confirmed, pending, cancelled), and an associated detail view action.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The six specified fields (Date, Client, Class Slot, Equipment, Status, View) are consistently displayed on page load, filter application, and filter clear — verified across at least three different filter combinations.
- **SC-002**: Zero regressions introduced to the Export PDF functionality — verified by comparing PDF output before and after the change.
- **SC-003**: The fix does not increase page load time by more than 5% compared to the current baseline.

## Assumptions

- The existing filter mechanism (API calls, client-side rendering) remains unchanged — only the column/field rendering logic is modified.
- The View button is considered a "field" for display consistency purposes (it is a per-row action).
- The reservations list uses a table or list format where columns/fields can be controlled independently from the data returned by the backend.
- No backend changes are required — the issue is isolated to the frontend rendering layer.
- Mobile/responsive views should follow the same consistency rule, but the exact field order or visibility on very small screens may adapt to fit the viewport.
