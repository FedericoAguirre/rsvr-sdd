# Feature Specification: Extend Filter Highlighting to Email and Mobile

**Feature Branch**: `017-filter-highlighting-extend`

**Created**: 2026-06-20

**Status**: Draft

**Input**: User description: "Add highlighting to email and mobile search results on the /clients page, matching the existing name-search highlighting behavior"

## Clarifications

### Session 2026-06-20

- Q: How should mobile number matching handle non-numeric formatting characters? → A: Strip all non-numeric characters from both search term and stored value before matching; highlight the matched portion in the formatted display value.

## User Scenarios & Testing

### User Story 1 - Email search shows highlighted results (Priority: P1)

An Operator searches for a client by email address and sees the matching portion of the email highlighted in the results, making it clear why each result was returned.

**Why this priority**: Core feature — without email highlighting, the feature has no value.

**Independent Test**: Can be tested by searching for a partial email address and verifying the matched fragment is visually distinct in each result.

**Acceptance Scenarios**:

1. **Given** the Operator searches by email address on the /clients page, **When** results are displayed, **Then** the matched portion of the email is visually highlighted (bold text + background color, consistent with name search)
2. **Given** the Operator types a partial email in uppercase, **When** the search executes, **Then** the matching portion is highlighted regardless of case (e.g., "JOHN" matches "john@example.com")
3. **Given** the Operator searches by email using fewer than 3 characters, **When** they pause, **Then** no email search highlighting is triggered

---

### User Story 2 - Mobile number search shows highlighted results (Priority: P1)

An Operator searches for a client by mobile number and sees the matching portion of the number highlighted in the results.

**Why this priority**: Core feature — without mobile number highlighting, the feature has no value.

**Independent Test**: Can be tested by searching for a partial mobile number and verifying the matched fragment is visually distinct in each result.

**Acceptance Scenarios**:

1. **Given** the Operator searches by mobile number on the /clients page, **When** results are displayed, **Then** the matched portion of the mobile number is visually highlighted (bold text + background color, consistent with name search)
2. **Given** the Operator types a partial mobile number (e.g., "555"), **When** the search executes, **Then** any mobile number containing "555" is returned with that portion highlighted

---

### User Story 3 - Consistency with existing name search highlighting (Priority: P2)

The highlighting behavior for email and mobile searches is visually identical to the existing name search highlighting, providing a consistent user experience.

**Why this priority**: Consistency is important for usability but not critical for initial functionality.

**Independent Test**: Can be tested by comparing the visual treatment of highlighted text across name, email, and mobile search results.

**Acceptance Scenarios**:

1. **Given** the Operator searches by name, email, or mobile, **When** results are displayed, **Then** the highlight style (bold, background color, contrast) is identical across all search types
2. **Given** the existing name search highlighting uses a specific visual treatment, **When** email or mobile search is performed, **Then** the same treatment is applied

---

### User Story 4 - All search fields remain functional (Priority: P2)

Existing name search highlighting and all other search functionality continues to work unchanged.

**Why this priority**: Regression prevention — Operators rely on all existing search capabilities.

**Independent Test**: Can be tested by performing a name search and verifying highlighting still works as before.

**Acceptance Scenarios**:

1. **Given** the Operator performs a name search, **When** results are displayed, **Then** the matched name portion is still highlighted as before
2. **Given** the Operator switches between name, email, and mobile search, **When** each search executes, **Then** results display with correct highlighting for each field

### Edge Cases

- What happens when the email contains the search term in the local part but not the domain? Only the matching local part is highlighted.
- What happens when the mobile number contains special characters (spaces, dashes, parentheses)? Non-numeric characters are stripped for matching; highlighting is applied to the matched digit sequence in the formatted display value.
- What happens when the Operator clears the search field? The highlighting is removed along with the search results.
- What happens when both name and email/mobile are searched together? All matching fields should show highlighting where applicable.

## Requirements

### Functional Requirements

- **FR-001**: The email search results on the /clients page MUST display the matching search term highlighted in each returned email address
- **FR-002**: The mobile number search results on the /clients page MUST display the matching search term highlighted in each returned mobile number
- **FR-003**: The highlighting visual treatment for email and mobile results MUST match the existing name search highlighting (bold text + background color)
- **FR-004**: The highlighting MUST be case-insensitive for email searches
- **FR-005**: The highlighting MUST support partial (substring) matches for both email and mobile searches
- **FR-006**: The existing name search highlighting MUST continue to work unchanged
- **FR-007**: The minimum character threshold for triggering highlighting MUST be the same as the existing search threshold (3 characters)
- **FR-008**: The search results MUST update dynamically as the Operator types (debounce behavior consistent with existing implementation)
- **FR-009**: The highlighting MUST follow WCAG 2.1 AA accessibility standards (sufficient color contrast, screen reader announcements)
- **FR-010**: For mobile number searches, the system MUST strip all non-numeric characters from both the search term and stored values before matching, then highlight the matched portion in the formatted display value

### Key Entities

- **Client**: The entity being searched. Key attributes relevant to this feature include email and mobile number. Existing attributes (name, etc.) remain unchanged.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator searching by email sees the matched portion of the email highlighted in every result, regardless of case
- **SC-002**: An Operator searching by mobile number sees the matched portion of the number highlighted in every result
- **SC-003**: The highlight visual treatment (bold + background color) is identical across name, email, and mobile searches
- **SC-004**: All existing name search highlighting scenarios continue to pass after the change
- **SC-005**: Search results still update dynamically with no full-page reload required

## Assumptions

- The existing /clients page with name search highlighting is already in place (as described in specs/005-add-client-search)
- The same debounce behavior (~300ms) applies to email and mobile search
- The same minimum character threshold (3 characters) applies to email and mobile search triggering
- Email matching is case-insensitive (consistent with name search behavior)
- Mobile number matching strips all non-numeric characters from both search term and stored values before matching (as clarified in Session 2026-06-20)
- The existing search interface already supports selecting between name, email, and mobile search modes
- Authentication and authorization are already handled by the existing system
