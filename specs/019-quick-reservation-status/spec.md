# Feature Specification: Quick Reservation Status Management

**Feature Branch**: `019-quick-reservation-status`

**Created**: 2026-06-22

**Status**: Draft

**Input**: User description: "Quickly mark reservations as used or unused directly from the reservation list view, row by row"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mark a reservation as used from the list view (Priority: P1)

As an Operator, I want to mark a reservation as "used" from the reservation list so I can quickly record that a climber attended their session without navigating to a detail page.

**Why this priority**: Marking reservations as "used" is the core daily task for operators managing check-ins. It is the primary action this feature enables.

**Independent Test**: Can be fully tested by opening the reservation list, clicking the "used" action on any reservation, and verifying the status badge updates to "used" without a page reload.

**Acceptance Scenarios**:

1. **Given** a reservation list with a reservation that has "reserved" status, **When** the operator clicks the "Mark as used" action on that row, **Then** the reservation status changes to "used" and the badge updates to the "used" color (blue).
2. **Given** a reservation list with a reservation that has "unused" status, **When** the operator clicks the "Mark as used" action on that row, **Then** the reservation status changes to "used" and the badge updates accordingly.

---

### User Story 2 - Mark a reservation as unused from the list view (Priority: P1)

As an Operator, I want to mark a reservation as "unused" from the reservation list so I can quickly record a no-show or cancellation without navigating to a detail page.

**Why this priority**: This is equally critical to the "mark as used" action — both form the complete set of status-change operations an operator needs at a glance.

**Independent Test**: Can be fully tested by opening the reservation list, clicking the "unused" action on any reservation, and verifying the status badge updates to "unused" without a page reload.

**Acceptance Scenarios**:

1. **Given** a reservation list with a reservation that has "reserved" status, **When** the operator clicks the "Mark as unused" action on that row, **Then** the reservation status changes to "unused" and the badge updates to the "unused" color (gray).
2. **Given** a reservation list with a reservation that has "used" status, **When** the operator clicks the "Mark as unused" action on that row, **Then** the reservation status changes to "unused" and the badge updates accordingly.

---

### User Story 3 - View reservation status badges at a glance (Priority: P2)

As an Operator, I want to see the current status of each reservation as a colored badge in the list so I can quickly identify which climbers have checked in, which did not show, and which are still pending.

**Why this priority**: Status badges support the core action by providing visual context. Without them, the operator would need to read text labels to understand each reservation's state, slowing down the workflow.

**Independent Test**: Can be tested by loading a reservation list with reservations in all three states and verifying each shows the correct badge color: green for reserved, blue for used, gray for unused.

**Acceptance Scenarios**:

1. **Given** a reservation list with at least one reservation in each status (reserved, used, unused), **When** the operator views the list, **Then** each reservation displays a colored badge matching its status (green=reserved, blue=used, gray=unused).
2. **Given** a reservation list where a status has just been changed via inline action, **When** the row updates, **Then** the badge shows the new status with the correct color immediately.

### Edge Cases

- What happens when the operator clicks "Mark as used" or "Mark as unused" on a reservation that has already reached its maximum capacity or session start time? The status change should still be allowed — the operator is recording attendance, not modifying availability.
- What happens if the network request fails during a status change? The row should revert to its previous state and display an error indication so the operator knows to retry.
- What happens when a reservation's status is already the target status (e.g., marking a "used" reservation as "used")? The system should gracefully handle this as a no-op or display a message indicating no change is needed.
- How does the status change interact with concurrent operators? If two operators attempt to change the status of the same reservation simultaneously, the last successful request wins and the row updates accordingly.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each reservation row in the list view MUST display a colored status badge showing its current status. The badge colors MUST be: green for "reserved", blue for "used", gray for "unused".
- **FR-002**: Each reservation row in the list view MUST provide inline action buttons to change the reservation status to "used" or "unused" without navigating to a detail page.
- **FR-003**: The "Mark as used" action MUST only be available when the reservation status is "reserved" or "unused". It SHOULD be hidden or disabled when the status is already "used".
- **FR-004**: The "Mark as unused" action MUST only be available when the reservation status is "reserved" or "used". It SHOULD be hidden or disabled when the status is already "unused".
- **FR-005**: When a status change action is triggered, the corresponding row MUST update in-place to reflect the new status and badge without requiring a full page reload.
- **FR-006**: If a status change request fails (network error, server error), the row MUST revert to its previous state and MUST display a visual error indicator so the operator is aware the change did not persist.
- **FR-007**: Status changes MUST be recorded per-reservation (single row). The system MUST NOT change the status of other reservations when a single row action is performed.
- **FR-008**: The status badge colors MUST be visually distinct and clearly legible against the row background.

### Key Entities *(include if feature involves data)*

- **Reservation**: Represents a climber's booking for a specific session or slot. Key attribute: `status` — a value that can be "reserved", "used", or "unused". Each reservation appears as a single row in the list view.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can mark a reservation as used or unused in 2 clicks or fewer, without leaving the reservation list view.
- **SC-002**: Status changes are reflected visually within 1 second of clicking the action button, providing near-instant feedback.
- **SC-003**: Operators can identify the status of any reservation at a glance without reading text labels, using colored badges.
- **SC-004**: Status changes affect only the target reservation — no other rows or data are modified.

## Assumptions

- Operators are using a desktop or tablet browser with JavaScript enabled (required for inline dynamic row updates).
- The existing reservation status change endpoint (used for detail-page operations) will be reused for inline actions.
- The three status values are "reserved", "used", and "unused" — no additional statuses are introduced.
- Mobile support is in scope for viewing but inline actions should degrade gracefully on small screens.
- The operator is authenticated and has permission to modify reservation statuses.
