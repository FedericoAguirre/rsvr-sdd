# Feature Specification: Add Client Search by Name

**Feature Branch**: `005-add-client-search`

**Created**: 2026-06-13

**Status**: Draft

**Input**: User description: "Add search client by name feature. As an Operator I want to be able to search a Client by name. Keeping the actual search options by email or mobile number. I want to use at least 3 letters, to start the search. The search must be case insensitive."

## Clarifications

### Session 2026-06-13

- Q: How does the search trigger? → A: Real-time on each keystroke with a short debounce (~300ms).
- Q: What visual treatment for matched text? → A: Bold text + background color.
- Q: How should results be sorted? → A: Alphabetical by name (first name then last name).
- Q: Expected number of clients? → A: Up to 1,000.
- Q: Accessibility requirements? → A: Follow WCAG 2.1 AA (screen reader announcements, keyboard navigation, sufficient color contrast).

## User Scenarios & Testing

### User Story 1 - Search client by name (Priority: P1)

An Operator types a client's name (or partial name) into the search box on the `clients/search/` page and sees matching client results. The search is case insensitive and requires at least 3 characters before it activates.

**Why this priority**: Core feature — without name search, the feature has no value.

**Independent Test**: Can be tested by entering a partial client name (3+ characters) in the search field and verifying matching clients appear in the results.

**Acceptance Scenarios**:

1. **Given** the Operator is on the `clients/search/` page, **When** they type 3 or more characters of a client's name in the search field, **Then** clients whose name contains those characters (case insensitive) are shown in the results list
2. **Given** the Operator types a partial name using uppercase letters, **When** the search executes, **Then** results include clients whose name matches in any case (e.g., "MAR" matches "María", "mark", "MARTIN")
3. **Given** the Operator has typed fewer than 3 characters, **When** they pause, **Then** no name-based search is triggered

---

### User Story 2 - See search term highlighted in results (Priority: P1)

When results are displayed, the matching portion of each client name is visually highlighted so the Operator can quickly see why each result was returned.

**Why this priority**: Visual feedback confirms the search worked correctly and helps Operators scan results.

**Independent Test**: Can be tested by searching for a name fragment and verifying that fragment is visually distinct (colored/highlighted) in each returned client name.

**Acceptance Scenarios**:

1. **Given** search results are displayed, **When** the Operator views the list, **Then** the matching search term is highlighted in each client name
2. **Given** a client name matches in lowercase while the search was typed in uppercase, **When** the result is shown, **Then** the matched portion is highlighted regardless of case

---

### User Story 3 - No results handling (Priority: P1)

When no client matches the search criteria, the Operator sees a clear message indicating no results were found.

**Why this priority**: Clear feedback prevents Operator confusion when a search yields no results.

**Independent Test**: Can be tested by entering a name fragment that does not match any existing client and verifying a "Client NOT FOUND" message appears.

**Acceptance Scenarios**:

1. **Given** the Operator has entered a search term that matches no client, **When** the search executes, **Then** an alert/message displays: "Client NOT FOUND"
2. **Given** a "Client NOT FOUND" message is displayed, **When** the Operator modifies their search term, **Then** the message is replaced by new results or remains if still no match

---

### User Story 4 - Search by email or mobile still works (Priority: P2)

The existing search capabilities (by email address or mobile number) continue to function alongside the new name search.

**Why this priority**: Regression prevention — existing operators rely on email and mobile search.

**Independent Test**: Can be tested by searching for an email or mobile number that exists in the system and verifying the corresponding client appears in results.

**Acceptance Scenarios**:

1. **Given** the Operator searches by a client's email address, **When** the search executes, **Then** the matching client is shown in results
2. **Given** the Operator searches by a client's mobile number, **When** the search executes, **Then** the matching client is shown in results
3. **Given** the Operator searches by a combination of name and email, **When** the search executes, **Then** clients matching all criteria are shown

### Edge Cases

- What happens when the Operator types exactly 3 characters that match many clients? All matching clients are displayed.
- What happens when the Operator types more than 3 characters that partially match? Only clients with names containing the full typed fragment are returned.
- What happens when a client name contains special characters (accents, hyphens)? The search should match the stored name as-is.
- What happens when the search field is cleared? The results should return to the default state (e.g., full client list if available).

## Requirements

### Functional Requirements

- **FR-001**: The search on `clients/search/` MUST support searching clients by name using a partial, case-insensitive match
- **FR-002**: The name search MUST require a minimum of 3 characters before executing
- **FR-003**: The existing search by email address and mobile number MUST continue to work unchanged
- **FR-004**: The matching portion of the client name in search results MUST be visually highlighted with bold text and a background color
- **FR-005**: When no client matches the search criteria, the system MUST display a "Client NOT FOUND" message
- **FR-006**: Search results MUST update dynamically as the Operator types, triggered on each keystroke with a short debounce (~300ms), without requiring a full page reload
- **FR-007**: The system MUST search across both first name and last name fields
- **FR-008**: Search results MUST be sorted alphabetically by first name, then last name
- **FR-009**: The search interface MUST follow WCAG 2.1 AA standards: dynamic results must be announced to screen readers, all controls must be keyboard-accessible, and highlight colors must meet minimum contrast ratios

### Key Entities

- **Client**: The entity being searched. Key attributes used for name search include first_name and last_name. Existing attributes (email, mobile, etc.) remain unchanged.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator can find any client by typing 3+ characters of their first or last name and see results within 2 seconds
- **SC-002**: Search results update dynamically as the Operator types, with no full-page reload required
- **SC-003**: The matched search term is visually highlighted in every result name, regardless of case
- **SC-004**: A clear "Client NOT FOUND" message appears within 1 second when no results match
- **SC-005**: All existing email and mobile search queries return the same results as before the change

## Assumptions

- The existing `clients/search/` endpoint, search interface, and Client model are already in place
- Client names are stored as first_name and last_name fields in the database
- Authentication and authorization are already handled by the existing system
- The existing email and mobile search continue to use their current matching logic unchanged
- The dynamic search behavior (no full page reload) is part of the feature scope
- The Operator role has permission to search and view clients
- The expected client database size is up to 1,000 records
