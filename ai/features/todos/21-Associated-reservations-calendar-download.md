# Feature Specification: Associated Reservations Calendar Download

**Feature Branch**: `021-associated-reservations-calendar-download`

**Created**: 2026-07-21

**Status**: Draft

**Input**: User description: "Download a calendar from the payment detail page with associated reservations, similar to the class calendar feature at specs/021-send-class-calendar/spec.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Download ICS Calendar from Payment Detail Page (Priority: P1)

As an operator, I want to download an ICS calendar file from the payment detail page containing all reservations associated with that payment, so that I can share the client's schedule and payment info with them.

**Why this priority**: This is the core feature — enabling operators to export a combined calendar of reservations linked to a payment for client delivery.

**Independent Test**: Can be fully tested by navigating to a payment detail page with associated reservations, clicking download, and receiving a valid ICS file with the correct naming convention.

**Acceptance Scenarios**:

1. **Given** I am on the payment detail page at `payments/{id}/`, **When** I click "Descargar calendario", **Then** an ICS file is downloaded.

2. **Given** the payment has associated reservations, **When** I open the downloaded ICS file in a calendar application, **Then** each associated reservation appears as an event containing the client name, class slot name, date, reserved equipment, and payment identifier.

3. **Given** the ICS file is downloaded, **When** I inspect the filename, **Then** it follows the format `<client_name>_<payment_identifier>_<first_reservation_date>_<last_reservation_date>.ics`, where dates are formatted as `YYYYMMDD` and client_name is in snake_case.

---

### User Story 2 — Handle Payment Without Reservations (Priority: P2)

As an operator, I want to receive clear feedback when a payment has no associated reservations, so that I understand the calendar is empty rather than receiving a broken or empty file.

**Why this priority**: Prevents confusion and ensures the operator knows the result of their action when there is no data to export.

**Independent Test**: Can be tested by viewing a payment with zero associated reservations and verifying that a meaningful message is shown instead of a download.

**Acceptance Scenarios**:

1. **Given** the payment has no associated reservations, **When** I click "Descargar calendario", **Then** a message is displayed indicating that no reservations are associated with this payment.

---

### Edge Cases

- What happens when the payment identifier contains special characters? The filename conversion must handle these gracefully.
- What happens if the client name has accents or special characters? Snake_case conversion must normalize these to valid ASCII.
- What happens if no reservations exist? A clear message is shown; no file is generated.
- What happens when there is a single reservation? The filename uses the same date for both first and last reservation date.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a "Descargar calendario" button on the payment detail page at `payments/{id}/`.
- **FR-002**: The system MUST generate an ICS file containing calendar events for all reservations associated with the payment.
- **FR-003**: Each ICS calendar event MUST include the client name, class slot name, class slot date, reserved equipment, and payment identifier in its event description.
- **FR-004**: The ICS file MUST include an additional field called "Pago" in each event containing the payment identifier.
- **FR-005**: The ICS file MUST be downloadable with the filename format `<client_name>_<payment_identifier>_<first_reservation_date>_<last_reservation_date>.ics`, where client_name is the snake_case version of the client's name, first_reservation_date is the earliest reservation date (YYYYMMDD), and last_reservation_date is the latest reservation date (YYYYMMDD).
- **FR-006**: If the payment has no associated reservations, the system MUST display a clear message and MUST NOT generate a downloadable file.
- **FR-007**: The download action MUST be idempotent — clicking the button multiple times generates the same calendar content for the same payment.

### Key Entities *(include if feature involves data)*

- **Payment**: A financial transaction record with a unique identifier, associated with a client and a set of reservations.
- **Reservation**: A booking record linking a client, equipment, class slot, and date — associated with a payment.
- **Client**: The person associated with the payment and reservations. Their name is used in the filename (snake_case).
- **Class Slot**: The scheduled time slot for a reservation, included in the calendar event details.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator can download the calendar from the payment detail page in 2 clicks or fewer.
- **SC-002**: The downloaded ICS file can be opened without errors in major calendar applications (Apple Calendar, Google Calendar, Outlook).
- **SC-003**: Each calendar event accurately reflects the corresponding reservation data, including the payment identifier.
- **SC-004**: The ICS file is generated within 3 seconds for a payment with up to 20 associated reservations.
- **SC-005**: When no reservations exist, the user sees an informative message within 3 seconds with no file downloaded.

## Assumptions

- The payment detail page at `payments/{id}/` already exists and lists associated reservations.
- Reservations associated to a payment include the necessary fields: client name, class slot name, date, and equipment.
- Client names can be programmatically converted to snake_case (spaces to underscores, lowercase, special characters simplified).
- Standard ICS (iCalendar) format is used, compatible with most calendar applications.
- The operator is already authenticated and authorized to view payment details.
- The icalendar library is available in the project dependencies.
