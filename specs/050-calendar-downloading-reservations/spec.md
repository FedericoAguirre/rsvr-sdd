# Feature Specification: Calendar Downloading in Reservations Page

**Feature Branch**: `050-calendar-downloading-reservations`

**Created**: 2026-07-21

**Status**: Draft

**Input**: User description: "As an operator, I want to download the calendar with the Payment Identificador, so that I can track down the client's paid reservations."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download Calendar from Reservations List (Priority: P1)

An operator filters reservations by a date range on the reservations page and clicks a "Download Calendar" button. The system generates an ICS file containing all reservations in that date range, with each event description including the client name, class slot, date, equipment, and the payment identifier.

**Why this priority**: This is the primary workflow — operators need calendar data for tracking paid reservations.

**Independent Test**: Can be fully tested by visiting the reservations page, setting a date range, clicking download, and verifying the ICS file includes all expected reservations with payment identifiers.

**Acceptance Scenarios**:

1. **Given** reservations exist within a specified date range, **When** the operator clicks "Download Calendar", **Then** an ICS file is downloaded containing one event per reservation.
2. **Given** a reservation is associated with a payment, **When** the ICS is generated, **Then** the event description includes the payment identifier.
3. **Given** the operator does not specify a date range, **When** they click "Download Calendar", **Then** the system shows an error or prompts for a date range.

---

### User Story 2 - Handle Unassociated Reservations (Priority: P2)

Reservations not linked to any payment should still appear in the calendar, with a clear indication that the payment is unassociated.

**Why this priority**: All reservations should be visible in the calendar even if no payment record exists yet.

**Independent Test**: Can be tested by creating reservations without payment association and verifying the ICS includes them with "Reservación sin asociar" as the payment identifier.

**Acceptance Scenarios**:

1. **Given** a reservation is not associated to any payment, **When** the ICS is generated, **Then** the payment identifier field shows "Reservación sin asociar".
2. **Given** multiple reservations, some associated and some not, **When** the ICS is generated, **Then** all reservations appear with their respective payment identifiers.

---

### User Story 3 - Multiple Payments in Date Range (Priority: P2)

A date range may span reservations belonging to different payments, and all should be included in a single ICS file.

**Why this priority**: Operators filter by date range, not by payment, so the calendar must handle mixed payment data.

**Independent Test**: Can be tested by creating reservations across two different payments within the same date range, downloading the calendar, and verifying all appear.

**Acceptance Scenarios**:

1. **Given** a date range spans reservations from multiple payments, **When** the ICS is generated, **Then** all reservations across those payments are included.
2. **Given** reservations from different payments, **When** the ICS is generated, **Then** each event shows its correct payment identifier.

---

### Edge Cases

- What happens when the date range contains no reservations? The system returns an empty ICS file or shows a message.
- What happens when a reservation is deleted between viewing the page and downloading? The system generates the ICS based on current data at download time.
- How does the system handle very large date ranges (e.g., a full year)? The ICS should include all reservations without performance issues.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Download Calendar" button on the reservations list page.
- **FR-002**: System MUST accept a date range (start date and end date) as input for the calendar download.
- **FR-003**: System MUST generate an ICS file containing one event per reservation within the date range.
- **FR-004**: Each ICS event description MUST include: client name, class slot, date, equipment, and payment identifier.
- **FR-005**: If a reservation has no associated payment, the payment identifier MUST display "Reservación sin asociar".
- **FR-006**: System MUST include all reservations from the date range regardless of which payment they belong to.
- **FR-007**: The ICS filename MUST be descriptive (e.g., include client name and date range).
- **FR-008**: System MUST handle empty date ranges gracefully (e.g., empty ICS or user message).
- **FR-009**: The existing ICS generation logic SHOULD be extracted into a shared utility to avoid duplication across clients, payments, and reservations apps.

### Key Entities *(include if feature involves data)*

- **Reservation**: A class booking linked to a client, class slot, date, equipment, and optionally a payment.
- **Payment**: A payment record that may be associated with one or more reservations.
- **Calendar File (ICS)**: The generated calendar file containing reservation events.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can download a calendar from the reservations page in under 2 clicks from viewing the list.
- **SC-002**: All reservations in the selected date range appear in the ICS file, including those without associated payments.
- **SC-003**: The calendar download does not increase page load time for the reservations list (generation happens on download, not on page load).
- **SC-004**: No duplicate ICS generation logic exists — the shared utility is used by all three apps (clients, payments, reservations).

## Assumptions

- The existing `_generate_ics` function in `clients/views.py` will be refactored into a shared utility accessible to all apps.
- The reservations page currently has date range filter inputs that can be reused for the calendar download.
- ICS timezone will remain `America/Denver` as in the existing implementation.
- Event duration is 1 hour per reservation, matching the current convention.
- Internet connection is available for downloading the file (no offline caching required).
