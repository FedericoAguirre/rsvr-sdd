# Feature Specification: Remove Status Buttons from Reservation List

**Feature Branch**: `020-remove-status-buttons`

**Created**: 2026-06-22

**Status**: Draft

**Input**: User description: "In the reservations/ webpage remove the used and unsed buttons functionality"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — View reservation list without inline status actions (Priority: P1)

Operators view the reservation list page and see status badges for each reservation. Previously there were "Used" and "Unused" buttons next to each row that allowed changing status without navigating away. These buttons have been removed, so operators must go to the reservation detail page to change a reservation's status.

**Why this priority**: This is the only user-facing change — removing the inline action buttons. No alternative flow exists for this view.

**Independent Test**: Can be verified by loading the reservation list page and confirming no "Used" or "Unused" buttons appear in any row.

**Acceptance Scenarios**:

1. **Given** the reservation list page is loaded, **When** the user views any reservation row, **Then** there is no "Used" or "Unused" button present
2. **Given** the reservation list page is loaded, **When** the user views any reservation row, **Then** the status badge is still displayed
3. **Given** the user navigates to a reservation's detail page, **When** they view the page, **Then** the existing status change functionality (used/unused) is still available

### Edge Cases

- Reservation rows rendered via HTMX partial swaps should also not contain the buttons
- The reservation list filtered by slot view should also not contain the buttons
- If no reservations exist, the "No reservations found." message should display normally without buttons

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The "Used" button MUST NOT appear in any reservation row in the main list view
- **FR-002**: The "Unused" button MUST NOT appear in any reservation row in the main list view
- **FR-003**: The "Used" button MUST NOT appear in any reservation row in the filtered-by-slot view
- **FR-004**: The "Unused" button MUST NOT appear in any reservation row in the filtered-by-slot view
- **FR-005**: The "Used" button MUST NOT appear in HTMX-swapped reservation row partials
- **FR-006**: The "Unused" button MUST NOT appear in HTMX-swapped reservation row partials
- **FR-007**: Status badges MUST continue to display in all reservation list views
- **FR-008**: The reservation detail page MUST retain its existing status change functionality

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: No "Used" or "Unused" buttons appear in any reservation list view (main, filtered-by-slot, or HTMX partial)
- **SC-002**: Status badges remain visible for all reservations in all list views
- **SC-003**: All existing tests continue to pass without modification

## Assumptions

- The reservation detail page's existing status change forms (within `<form>` elements with their own `{% csrf_token %}`) are unaffected and remain functional
- The `reservation_change_status` view and `/status/` URL route are preserved for the detail page's use
- Status badges add useful information and should be retained
