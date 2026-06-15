# Feature Specification: Remove Email from Client Column in Reservations List

**Feature Branch**: `009-remove-email-from-list`

**Created**: 2026-06-14

**Status**: Draft

**Input**: User description: "In the reservations/list endpoint, remove the email from the user name column"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admin views reservations list without email clutter (Priority: P1)

An admin opens the reservations list page to see which equipment is booked by whom. Each row shows the client's full name alongside the equipment name, without distracting email addresses in parentheses.

**Why this priority**: This is the only user-facing change requested. It cleans up the UI for daily reservation management.

**Independent Test**: Can be fully tested by loading any reservations list page and verifying the client column shows only the first and last name, with no email address visible.

**Acceptance Scenarios**:

1. **Given** a reservation exists for a client with an email address, **When** the reservations list page is rendered, **Then** the client column displays only the client's first and last name without the email address.
2. **Given** a reservation exists for a client without an email but with a mobile number, **When** the reservations list page is rendered, **Then** the client column displays only the client's first and last name without any contact information.
3. **Given** a reservation exists for a client with no email and no mobile, **When** the reservations list page is rendered, **Then** the client column displays only the client's first and last name without any fallback text.

---

### Edge Cases

- What happens when a client has only one name (first or last missing)? The column should display whatever name parts exist, with no contact info appended.
- Should the PDF export also exclude email from the client column? Yes — the change should apply consistently to all reservations list views including the PDF.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The reservations list page MUST display the client's full name (first and last name) without the email address or any other contact information in the client column.
- **FR-002**: The reservations list page by class slot MUST display the client's full name without contact information.
- **FR-003**: The reservations PDF export MUST display the client's full name without contact information.
- **FR-004**: The change MUST NOT affect the Client model's string representation (`__str__`) in other parts of the system where email may still be useful for disambiguation.

### Key Entities *(include if feature involves data)*

- **Client**: Person who makes reservations; has first_name, last_name, email, mobile fields
- **Reservation**: Links a Client to an Equipment item for a specific ClassSlot and Date

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On each reservations list view (full list, by-slot, PDF), no email addresses or contact information appear in the client column.
- **SC-002**: All existing tests continue to pass after the change.
- **SC-003**: The Client model's `__str__` method remains unchanged so other views (e.g., client search, detail) still show contact info.

## Assumptions

- The email is currently shown because the reservations templates render `{{ r.client }}`, which calls the Client model's `__str__` method. The fix will be to use explicit field access (e.g., `{{ r.client.first_name }} {{ r.client.last_name }}`) in the templates rather than modifying the model.
- The Client column label ("Client" / "Cliente") is already correct and needs no change.
- All three template files that render the reservations list should be updated consistently.
