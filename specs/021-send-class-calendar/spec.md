# Feature Specification: Send Class Reservations Calendar to Client

**Feature Branch**: `021-send-class-calendar`

**Created**: 2026-06-22

**Status**: Draft

**Input**: User description: "Send the class reservations calendar to the client"

## User Scenarios & Testing

### User Story 1 — Download ICS Calendar for a Client (Priority: P1)

As an Operator, I want to download an ICS calendar file containing all class reservations for a specific client within a date range, so that I can share the client's schedule with them.

**Why this priority**: This is the primary feature — fulfilling the core Operator need to export and share client reservation schedules.

**Independent Test**: Can be fully tested by an Operator navigating to the client detail page, selecting start and end dates, clicking download, and receiving a valid ICS file.

**Acceptance Scenarios**:

1. **Given** I am on the client detail page, **When** I select a date range that contains reservations and click download, **Then** an ICS file is downloaded with the naming convention `cal_<client_snake_case_name>_<start_YYYYMMDD>_<end_YYYYMMDD>.ics`.

2. **Given** I am on the client detail page, **When** the downloaded ICS file is opened in a calendar application, **Then** each reservation appears as an event containing the client name, class slot name, class slot date, and reserved equipment.

3. **Given** I have downloaded ICS files for two different clients, **When** I inspect the filenames, **Then** each filename correctly reflects its respective client name in snake_case.

---

### User Story 2 — Handle Empty Date Range Gracefully (Priority: P2)

As an Operator, I want to receive clear feedback when no reservations exist in the selected date range, so that I understand the calendar is empty rather than receiving a broken or empty file.

**Why this priority**: Prevents confusion and ensures the Operator knows the result of their action even when there is no data.

**Independent Test**: Can be tested by selecting a date range with zero reservations and verifying that a meaningful message is shown instead of a download.

**Acceptance Scenarios**:

1. **Given** the selected date range has no reservations for the client, **When** I click download, **Then** a message is displayed indicating that no reservations exist in that range.

---

### User Story 3 — Date Range Selection with Validation (Priority: P3)

As an Operator, I want to select a valid date range before downloading, so that the ICS file contains precisely the reservations I intend to share.

**Why this priority**: Enables precise control over which reservations are included, but core download functionality works even with a default range.

**Independent Test**: Can be tested by selecting an end date before a start date and verifying that an appropriate validation message is shown.

**Acceptance Scenarios**:

1. **Given** the start date is after the end date, **When** I attempt to download, **Then** an error message is displayed asking me to correct the date range.

---

### Edge Cases

- What happens when a client has no reservations at all? The date range selector shows no downloadable result and a message is displayed.
- What happens if the client name contains special characters (accents, apostrophes, hyphens)? The snake_case conversion should handle these gracefully, resulting in a valid filename.
- What happens if the date range is very large (e.g., one year)? The system generates the ICS file with all reservations in that range; very large files should still download correctly.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST provide a date range selector (start date and end date inputs) on the client detail page.
- **FR-002**: The system MUST generate an ICS file containing calendar events for all reservations belonging to the selected client within the specified date range.
- **FR-003**: Each ICS calendar event MUST include the client name, class slot name, class slot date, and reserved equipment in its description or title.
- **FR-004**: The ICS file MUST be downloadable with the filename format `cal_<client_name>_<start_date>_<end_date>.ics`, where client_name is the snake_case version of the client's name, and dates are formatted as `YYYYMMDD`.
- **FR-005**: If no reservations exist for the selected client in the specified date range, the system MUST display a clear message and MUST NOT generate a downloadable file.
- **FR-006**: The system MUST validate that the start date is not after the end date and show an error message if validation fails.
- **FR-007**: The download action MUST be available from the `clients/{client_id}/` page.

### Key Entities

- **Client**: A person who makes class reservations. Identified by name, which is converted to snake_case for the filename.
- **Class Slot**: A scheduled class session with a specific date (and optionally time) that a client can be reserved for.
- **Reservation**: A booking linking a client to a class slot, optionally including reserved equipment.
- **Equipment**: Items reserved by the client for a class slot, included in the calendar event details.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator can navigate to a client detail page and download the calendar in 3 or fewer clicks.
- **SC-002**: The downloaded ICS file can be opened without errors in major calendar applications (Apple Calendar, Google Calendar, Outlook).
- **SC-003**: Each reservation in the ICS file accurately reflects the corresponding client name, class slot name, date, and reserved equipment from the system.
- **SC-004**: The ICS file is generated within 3 seconds for a date range containing up to 100 reservations.
- **SC-005**: When no reservations exist in the range, the user sees an informative message within 3 seconds, with no file downloaded.

## Assumptions

- Class slots include at least a date value (time is optional; if absent, all-day events are used).
- Client names can be programmatically converted to snake_case (spaces to underscores, lowercase, special characters simplified).
- The existing client detail page at `clients/{client_id}/` provides the context for adding the download feature.
- The Operator is already authenticated and authorized to view client details.
- Standard ICS (iCalendar) format is used, compatible with most calendar applications.
- The date range defaults are empty (not pre-filled) — the Operator must explicitly choose start and end dates.
