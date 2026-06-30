# Feature Specification: Payments Client Search

**Feature Branch**: `027-payments-client-search`

**Created**: 2026-06-29

**Status**: Draft

**Input**: User description: "Use the @ai/features/todos/11_Payments_client_search.md to create the specs for the new feature"

## User Scenarios & Testing

### User Story 1 - Search payments by client name (Priority: P1)

An Operator on the `payments/` page types a client's name (or partial name) into a search field and sees payments associated to matching clients. The search is case-insensitive and requires at least 3 characters before it activates.

**Why this priority**: Core feature — without name-based search the feature has no value.

**Independent Test**: Can be tested by entering a partial client name (3+ characters) in the search field and verifying payments for matching clients appear in the grid.

**Acceptance Scenarios**:

1. **Given** the Operator is on the `payments/` page, **When** they type 3 or more characters of a client's name in the search field, **Then** payments belonging to clients whose name contains those characters (case-insensitive) are shown in the payments grid
2. **Given** the Operator types a partial name using uppercase letters, **When** the search executes, **Then** results include payments of clients whose name matches in any case
3. **Given** the Operator has typed fewer than 3 characters, **When** they pause, **Then** no client name-based search is triggered and the grid shows all payments

---

### User Story 2 - Search payments by client email or mobile (Priority: P1)

An Operator searches payments by typing a client's email address or mobile number. The existing client search fields for email and mobile work alongside the new name search.

**Why this priority**: Email and mobile are existing search criteria from the client search feature and must continue working.

**Independent Test**: Can be tested by entering a client's email or mobile number and verifying the corresponding payments appear in the grid.

**Acceptance Scenarios**:

1. **Given** the Operator enters a client's complete or partial email address, **When** the search executes, **Then** payments of clients whose email matches are shown
2. **Given** the Operator enters a client's complete or partial mobile number, **When** the search executes, **Then** payments of clients whose mobile matches are shown
3. **Given** the Operator enters a combination of criteria (e.g., name + email), **When** the search executes, **Then** payments belonging to clients matching all criteria are shown

---

### User Story 3 - No results handling (Priority: P2)

When no payment matches the search criteria, the Operator sees a clear message indicating no results were found. The existing grid format is preserved.

**Why this priority**: Clear feedback prevents Operator confusion when a search yields no results.

**Independent Test**: Can be tested by entering a search term that matches no client and verifying a "NOT FOUND" message is displayed in the grid area.

**Acceptance Scenarios**:

1. **Given** the Operator has entered a search term that matches no client, **When** the search executes, **Then** a "NOT FOUND" message is displayed in place of grid rows
2. **Given** a "NOT FOUND" message is displayed, **When** the Operator clears or modifies the search term, **Then** matching results appear or the message remains if still no match

### Edge Cases

- What happens when the Operator types exactly 3 characters that match many clients? Payments for all matching clients are displayed.
- What happens when multiple clients share the same name? Payments for all matching clients are shown in the grid.
- What happens when a client has no payments? That client is simply not represented in the grid results.
- What happens when the search field is cleared? The grid returns to showing all payments (default state).
- What happens when the Operator searches for a term that matches the client but that client was soft-deleted? Soft-deleted clients are excluded from the search.

## Requirements

### Functional Requirements

- **FR-001**: The `payments/` page MUST include a search field that allows Operators to filter payments by client name, email address, or mobile number
- **FR-002**: The search MUST use partial, case-insensitive matching on client attributes (name, email, mobile)
- **FR-003**: The search MUST require a minimum of 3 characters before executing
- **FR-004**: The existing payments grid format and pagination MUST remain unchanged
- **FR-005**: When no payments match the search criteria, the system MUST display a "NOT FOUND" message in the grid area
- **FR-006**: Search results MUST update dynamically as the Operator types with a debounce (~300ms), and the Operator can also trigger the search explicitly via a search button or Enter key
- **FR-007**: The search MUST match against the client's full name (first name and last name combined)
- **FR-008**: The search MUST also match against the client's email address and mobile number as stored in the system

### Key Entities

- **Payment**: The record being displayed. Each payment is associated with a client. The grid shows payment records without modification.
- **Client**: The entity whose attributes (name, email, mobile) are used for filtering payments. Payments are filtered by finding clients matching the search criteria and showing only their associated payments.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator can find payments for a specific client by typing 3+ characters of their name, email, or mobile and see results within 2 seconds
- **SC-002**: Search results update dynamically as the Operator types, with no full-page reload required
- **SC-003**: The payments grid format, columns, and pagination remain identical to the pre-feature state
- **SC-004**: A clear "NOT FOUND" message appears within 1 second when no results match
- **SC-005**: All existing payment grid functionality (sort, pagination, row actions) continues to work unchanged

## Assumptions

- The existing `payments/` page, payment grid, and payment model are already in place
- Each payment is associated with a client record that has name, email, and mobile fields
- The client search feature (`specs/005-add-client-search/`) provides the reference UX pattern for the search UI (debounced input, minimum characters)
- Authentication and authorization are already handled by the existing system
- The expected volume of payments and clients is consistent with current system capacity
- Search only filters the existing payment queryset; no new data sources are needed
