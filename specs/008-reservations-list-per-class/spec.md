# Feature Specification: Create Reservations List per Class Slot

**Feature Branch**: `008-reservation-lists`

**Created**: 2026-06-14

**Status**: Draft

**Input**: User description: "create the spec from @ai/features/todos/01_create_reservations_list_per_class.md" and "Add the next spec @ai/features/todos/01a_Modify_reservations.md into the current feature"

## Clarifications

### Session 2026-06-14

- Q: Can one client reserve multiple equipment items and can multiple clients reserve the same equipment? → A: One Client can reserve only one piece of Equipment per class slot, and each Equipment can be reserved by only one Client per slot (1:1 mapping per slot).
- Q: Should cancelled or expired reservations appear in the list? → A: Show only active/confirmed reservations; exclude cancelled/expired.
- Q: Which user roles can access the reservations list? → A: Both Operators and Administrators can view and export the reservations list.
- Q: What happens if PDF export or data loading fails? → A: Show a user-friendly error message with a retry button.
- Q: What language/locale should the list header and UI use? → A: Use the system's configured language; display header labels and data as stored in the system.
- Q: (spec amendment) Modify main Reservations page with class slot filter and per-slot table → A: Integrated as User Story 3 (P2)

## User Scenarios & Testing

### User Story 1 - View reservations list for a class slot and date (Priority: P1)

An Operator or Administrator selects a Class slot and a date, and the system displays a list of all equipment reservations for that class slot on that date. The list includes the date and class slot name in the header, and shows a table of equipment names with the clients that reserved them, ordered by equipment name.

**Why this priority**: Core functionality — without being able to view the list, the feature has no value.

**Independent Test**: Can be tested by selecting any class slot and date with existing reservations and verifying the list displays correctly with header and ordered equipment names.

**Acceptance Scenarios**:

1. **Given** the Operator is on the reservations page, **When** they select a Class slot and a date that has reservations, **Then** the system displays a list with the date and class slot name in the header
2. **Given** the Operator views the reservations list, **When** equipment reservations exist for the selected slot and date, **Then** equipment names are displayed in alphabetical order with their corresponding client names
3. **Given** the Operator selects a Class slot and date with no reservations, **When** the list is displayed, **Then** the header is shown but the equipment table is empty
4. **Given** the Operator selects a Class slot and a date in the past, **When** reservations existed for that combination, **Then** the historical reservations list is displayed correctly

---

### User Story 2 - Export reservations list to PDF (Priority: P2)

An Operator or Administrator downloads the equipment reservations list for a given class slot and date as a PDF document for offline use, sharing, or record-keeping.

**Why this priority**: The PDF export adds practical utility but the feature is still valuable without it — the Operator can view the list on screen.

**Independent Test**: Can be tested by viewing a reservations list, clicking the export button, and verifying a PDF file is downloaded with the same content as the on-screen list.

**Acceptance Scenarios**:

1. **Given** the Operator is viewing a reservations list, **When** they click the export button, **Then** a PDF file is downloaded containing the same header and table data as the on-screen list
2. **Given** the Operator views an empty reservations list, **When** they export to PDF, **Then** the PDF is still generated with the header and an empty table

### User Story 3 - Modify main Reservations page with class slot filter (Priority: P2)

The main Reservations page (`/reservations/`) is updated to include a class slot filter alongside the existing date filter, and the table displays the reservation-list-by-slot data showing equipment names with their assigned clients. The "New Reservation" button is preserved.

**Why this priority**: Improves the existing workflow by integrating the per-slot list into the main page, but the separate `/reservations/list/` page already provides the functionality.

**Independent Test**: Navigate to `/reservations/` as an Operator — the page shows a class slot filter, date filter, "New Reservation" button, and a table of equipment-client pairs filtered by the selected class slot and date.

**Acceptance Scenarios**:

1. **Given** the Operator is on the main Reservations page, **When** they select a Class slot and date and apply the filter, **Then** the table displays equipment names and their corresponding client names ordered by equipment name
2. **Given** the Operator is on the main Reservations page, **When** no class slot or date filter is selected, **Then** the table shows all reservations (existing behavior)
3. **Given** the Operator is on the main Reservations page, **When** they view the page, **Then** the "New Reservation" button is visible and functional
4. **Given** the Operator is on the main Reservations page with a class slot filter active, **When** there are no reservations for the selected slot and date, **Then** the table is empty with an appropriate message

---

### Edge Cases

- What happens when a Class slot has no equipment reservations for the selected date? An empty list/table is shown with the header intact.
- What happens when multiple clients have reserved the same equipment? This does not occur — each piece of Equipment can be reserved by at most one Client per class slot.
- What happens if the Operator selects a future date with no reservations yet? The list shows an empty table — the Operator can still view and export it.
- What happens if the selected Class slot does not exist (e.g., was deleted)? The system should show an appropriate message rather than an empty or broken list.
- What happens if PDF export fails (e.g., network error, server timeout)? A user-friendly error message is displayed with a retry button.
- What happens when the main reservations page loads without any filters selected? All reservations are shown (existing behavior preserved).
- What happens if the class slot filter is changed while a date filter is already set? The table updates to show reservations matching both filters simultaneously.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST allow an Operator or Administrator to select a Class slot from the available slots
- **FR-002**: The system MUST allow an Operator to select or enter a date
- **FR-003**: The system MUST display a reservations list that includes the selected date and class slot name in the header
- **FR-004**: The system MUST display a table of equipment names with their corresponding client names, ordered alphabetically by equipment name
- **FR-005**: The system MUST allow the Operator to export the displayed reservations list as a PDF document
- **FR-006**: The exported PDF MUST contain the same date, class slot name, and equipment-client table as the on-screen view
- **FR-007**: The system MUST handle the case where no reservations exist for the selected combination by showing an empty table (with header still present)
- **FR-008**: The main Reservations page MUST include a class slot filter (dropdown) in addition to the existing date filter
- **FR-009**: When a class slot is selected as filter, the reservations table MUST display equipment names with client names ordered by equipment name (as in the per-slot list view)
- **FR-010**: The "New Reservation" button MUST remain visible and functional on the modified Reservations page

### Key Entities

- **Class Slot**: Represents a scheduled class time slot (e.g., "Morning Yoga", "Evening Climbing"). Identified by name and scheduled time.
- **Equipment**: A piece of gym equipment that can be reserved by clients. Key attributes: name, type, status.
- **Client**: A gym member or user who can reserve equipment. Key attributes: name, membership details.
- **Reservation**: The association between a Client, a piece of Equipment, and a Class Slot for a specific date. A Client may reserve at most one piece of Equipment per Class Slot per date, and each piece of Equipment may be reserved by at most one Client per Class Slot per date (1:1 mapping per slot). Each reservation has a status (active/confirmed or cancelled/expired). The reservations list shows only active/confirmed reservations.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator can view the equipment reservations list for any class slot and date combination in under 3 clicks from the main navigation
- **SC-002**: The reservations list displays results within 2 seconds for a class slot with up to 50 reservations
- **SC-003**: The PDF export completes within 5 seconds and downloads a correctly formatted document
- **SC-004**: Equipment names are consistently displayed in alphabetical order across all views and exports
- **SC-005**: An Operator can successfully view reservations lists for any combination of past, present, or future dates and class slots
- **SC-006**: An Operator can apply a class slot filter on the main Reservations page in 1 click from the page load
- **SC-007**: The main Reservations page preserves all existing functionality (date filter, New Reservation button, all-reservations table when unfiltered)

## Assumptions

- The Operator is already authenticated and has appropriate permissions to view reservations
- The data for Class slots, Equipment, Clients, and Reservations already exists in the system
- The interface is web-based (part of the existing management system)
- PDF generation uses a standard browser-based or server-side approach (e.g., print-to-PDF or PDF library)
- The existing class slot selection and date picker UI patterns are reused for this feature
- Alphabetical ordering follows standard lexicographic order by equipment name
- The list UI uses the system's configured language/locale for all header labels and messages
