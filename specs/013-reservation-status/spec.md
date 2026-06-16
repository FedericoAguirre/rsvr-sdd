# Feature Specification: Add Reservation Status

**Feature Branch**: `013-reservation-status`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "Add reservation status to a reservation"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mark Reservation as Used or Unused (Priority: P1)

As an Administrator or Operator, I want to mark a reservation as "used" when the client attended the class, or "unused" when they did not, so that I can track attendance accurately.

**Why this priority**: This is the core functionality of the feature. Without the ability to change status, no attendance tracking can occur.

**Independent Test**: An operator can navigate to a reservation, change its status to "used" and see the change reflected immediately. This delivers the primary value of attendance tracking.

**Acceptance Scenarios**:

1. **Given** a reservation with status "reserved", **When** an Administrator marks it as "used", **Then** the status changes to "used"
2. **Given** a reservation with status "reserved", **When** an Operator marks it as "unused", **Then** the status changes to "unused"
3. **Given** a reservation with status "used", **When** an Administrator marks it back to "reserved", **Then** the status changes to "reserved"
4. **Given** a reservation with status "unused", **When** an Operator marks it as "reserved", **Then** the status changes to "reserved"

---

### User Story 2 - View Reservation Status in Listings (Priority: P1)

As an Administrator or Operator, I want to see the reservation status displayed in the reservation list, so that I can quickly identify which clients attended and which did not.

**Why this priority**: Without visual status in listings, operators would have no efficient way to review attendance.

**Independent Test**: The reservation list shows a status column/value for every reservation with clear labels in Spanish.

**Acceptance Scenarios**:

1. **Given** the reservation list view, **When** viewing reservations, **Then** each reservation displays its current status
2. **Given** a reservation with status "used", **When** viewing it in the list, **Then** the status appears as "Usado"
3. **Given** a reservation with status "unused", **When** viewing it in the list, **Then** the status appears as "No usado"
4. **Given** a reservation with status "reserved", **When** viewing it in the list, **Then** the status appears as "Reservado"

---

### User Story 3 - Filter Reservations by Status (Priority: P2)

As an Administrator or Operator, I want to filter the reservation list by status, so that I can quickly see only pending, attended, or unattended reservations.

**Why this priority**: Filtering helps operators manage large volumes of reservations efficiently, but is not required for the basic status change functionality.

**Independent Test**: An operator can select a status filter and see only matching reservations.

**Acceptance Scenarios**:

1. **Given** the reservation list view with a status filter control, **When** selecting "Usado", **Then** only reservations with status "used" are shown
2. **Given** the reservation list view with a status filter control, **When** selecting "No usado", **Then** only reservations with status "unused" are shown
3. **Given** the reservation list view with a status filter control, **When** selecting "Reservado", **Then** only reservations with status "reserved" are shown
4. **Given** the reservation list view with a status filter, **When** clearing the filter, **Then** all reservations are shown regardless of status

---

### User Story 4 - Export Reservations with Status (Priority: P2)

As an Administrator or Operator, I want exported reservation reports (PDF) to include the status, so that I can share accurate attendance records.

**Why this priority**: Exports are important for reporting but the feature can be used without them initially.

**Independent Test**: Generate a PDF export of reservations and verify that the status column is present with correct values in Spanish.

**Acceptance Scenarios**:

1. **Given** a reservation with status "used", **When** exporting reservations to PDF, **Then** the export includes "Usado" in the status column
2. **Given** a reservation with status "unused", **When** exporting reservations to PDF, **Then** the export includes "No usado" in the status column
3. **Given** a reservation with status "reserved", **When** exporting reservations to PDF, **Then** the export includes "Reservado" in the status column

### Edge Cases

- What happens when a reservation is already marked "used" and the operator tries to mark it "used" again? The system should allow re-setting the same status without error.
- How does the system handle bulk operations across multiple reservations at once?
- What happens when a reservation for a past class slot is updated to "used" retroactively?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST assign "reserved" as the default status for all new reservations
- **FR-002**: Administrators and Operators MUST be able to change a reservation's status to "used"
- **FR-003**: Administrators and Operators MUST be able to change a reservation's status to "unused"
- **FR-004**: Administrators and Operators MUST be able to change a reservation's status back to "reserved"
- **FR-005**: System MUST display the reservation status in the reservation list view
- **FR-006**: System MUST display reservation status in exported PDF reports
- **FR-007**: System MUST support filtering the reservation list by status
- **FR-008**: System MUST display status labels in Spanish: "Reservado", "Usado", "No usado"
- **FR-009**: System MUST require authentication (Administrator or Operator role) to change reservation status

### Key Entities *(include if feature involves data)*

- **Reservation**: Represents a client's booking for a class slot. Each reservation has a status attribute that can be "reserved", "used", or "unused". Status defaults to "reserved" upon creation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can change a reservation's status in 2 clicks or fewer from the reservation detail view
- **SC-002**: Status changes are reflected in the reservation list immediately after saving
- **SC-003**: All reservation list views and PDF exports include status information
- **SC-004**: Filtering by status returns results in under 2 seconds
- **SC-005**: 100% of existing reservation list and export tests pass after adding status support

## Assumptions

- The system already has role-based access control distinguishing Administrators from Operators
- The reservation list and PDF export features exist and only need to be updated to include status
- The status is a simple string/enum field on the reservation entity
- The user interface language for Operators is Spanish (status labels must be translated)
- Bulk operations are out of scope for this feature
- Status changes are not automatically triggered — they are always manual by an authorized user
