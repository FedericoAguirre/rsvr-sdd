# Feature Specification: Payments Labels Change

**Feature Branch**: `032-payments-labels-change`

**Created**: 2026-07-09

**Status**: Draft

**Input**: User description: "In the payments/ webpage change labels: 'Filtrar por cliente' to 'Buscar Clientes', 'ID de cliente' to 'Buscar clientes...'. Reuse i18n labels from clients/search. Change 'Filtrar' button label to 'Buscar' and CSS class to btn-primary. Change 'Nuevo pago' button CSS class to btn-success."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Updated Payment Search Labels (Priority: P1)

As a user managing payments, I want the search client field and label to use the same wording as the clients search page, so that the interface is consistent across the application.

**Why this priority**: This is the primary change requested and affects the main search interface on the payments page.

**Independent Test**: Can be fully tested by navigating to the payments page and verifying the two label changes are displayed correctly, delivering immediate UI consistency.

**Acceptance Scenarios**:
1. **Given** I am on the payments page, **When** I view the client filter field, **Then** the label reads "Buscar Clientes" instead of "Filtrar por cliente"
2. **Given** I am on the payments page, **When** I view the client ID input placeholder, **Then** it reads "Buscar clientes..." instead of "ID de cliente"
3. **Given** I am on the payments page, **When** I inspect the label source, **Then** the labels are sourced from the same i18n translations used on the clients/search page

---

### User Story 2 - Updated Filter Button (Priority: P1)

As a user, I want the filter button to use the label "Buscar" with primary button styling, so that it is visually consistent with other search actions in the application.

**Why this priority**: This change is part of the core label update request and affects the primary action button on the page.

**Independent Test**: Can be fully tested by viewing the filter button on the payments page and verifying its label and style match the specification.

**Acceptance Scenarios**:
1. **Given** I am on the payments page, **When** I view the filter button, **Then** its label reads "Buscar" instead of "Filtrar"
2. **Given** I am on the payments page, **When** I inspect the filter button CSS classes, **Then** they include "btn btn-primary"

---

### User Story 3 - Updated New Payment Button Style (Priority: P2)

As a user, I want the "Nuevo pago" button to have success (green) styling, so that create actions are visually distinct from filter/search actions.

**Why this priority**: This is a visual enhancement that improves usability but is less critical than the label correctness.

**Independent Test**: Can be fully tested by viewing the "Nuevo pago" button on the payments page and verifying its CSS classes.

**Acceptance Scenarios**:
1. **Given** I am on the payments page, **When** I inspect the "Nuevo pago" button CSS classes, **Then** they include "btn btn-success"

---

### Edge Cases

- What happens if the i18n keys used on clients/search are not available in the payments page context? System should fall back to literal string values matching the expected labels.
- What happens if the payments page is rendered with no client filter visible (e.g., empty state)? The label changes should still apply to the underlying UI elements even if hidden.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The payments page MUST display the client filter label as "Buscar Clientes" instead of "Filtrar por cliente"
- **FR-002**: The payments page MUST display the client ID input placeholder as "Buscar clientes..." instead of "ID de cliente"
- **FR-003**: The client filter label and placeholder MUST reuse the same i18n translation keys used on the clients/search page
- **FR-004**: The filter/submit button label MUST display "Buscar" instead of "Filtrar"
- **FR-005**: The filter/submit button MUST have CSS classes "btn btn-primary"
- **FR-006**: The "Nuevo pago" button MUST have CSS classes "btn btn-success"

### Key Entities *(include if feature involves data)*

- **Payment**: Existing payment record entity; no new attributes required
- **Client**: Existing client record entity; used for search/filter functionality

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four label/text changes are correctly displayed on the payments page (client filter label, placeholder, filter button, new payment button)
- **SC-002**: The client filter label and placeholder text are visually and textually consistent with the clients/search page
- **SC-003**: The filter button is styled with primary (blue) visual treatment and the "Nuevo pago" button is styled with success (green) visual treatment
- **SC-004**: All changes are purely presentational — no existing functionality (search, filtering, payment creation) is altered

## Assumptions

- The existing i18n system uses shared translation keys that can be referenced from any template
- The clients/search page already has the desired "Buscar Clientes" and "Buscar clientes..." labels implemented via i18n
- The current button classes for "Filtrar" and "Nuevo pago" are CSS classes that can be safely replaced without affecting functionality
- No new translations or i18n keys need to be created — existing keys from clients/search will be reused
- The layout and structure of the payments page remain unchanged; only labels and CSS classes are modified
- All changes are client-side template/presentation changes only; no backend logic changes required
