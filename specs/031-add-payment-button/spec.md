# Feature Specification: Add Payment Button to Client Page

**Feature Branch**: `031-add-payment-button`

**Created**: 2026-07-08

**Status**: Draft

**Input**: Create the new feature specs from @ai/features/todos/04-payment-button-client.md

## User Scenarios & Testing

### User Story 1 - Create Payment from Client Detail Page (Priority: P1)

As a system user viewing a client detail page, I want to click a **New Payment** button so that I can navigate to the payment creation page with the current client preselected in the client combo box.

**Why this priority**: This is the primary user journey — the entire feature is adding this button with client preselection capability.

**Independent Test**: Can be fully tested by navigating to any client detail page at `clients/{client_id}/`, confirming the **New Payment** button appears to the right of the **Nueva Reserva** button, clicking it, and verifying the browser navigates to `payments/create/` with the client combo box already set to that client.

**Acceptance Scenarios**:

1. **Given** I am on the `clients/{client_id}/` detail page, **When** I view the action buttons, **Then** a **New Payment** button is displayed to the right of the **Nueva Reserva** button
2. **Given** I am on the `clients/{client_id}/` detail page, **When** I click the **New Payment** button, **Then** I am navigated to the `payments/create/` page
3. **Given** I am on the `payments/create/` page after clicking the **New Payment** button, **When** the page loads, **Then** the client combo box is preselected with the client that was viewed on the previous page

---

### User Story 2 - Create Payment with No Client (Direct Access) (Priority: P2)

As a system user, I want to navigate directly to the `payments/create/` page so that I can create a payment without a preselected client.

**Why this priority**: The direct-access flow must continue to work as it did before this feature; this story verifies no regression.

**Independent Test**: Can be fully tested by navigating directly to `payments/create/` and confirming the client combo box is empty and the user can select a client manually to create the payment.

**Acceptance Scenarios**:

1. **Given** I navigate directly to `payments/create/`, **When** the page loads, **Then** the client combo box is empty (no client preselected)
2. **Given** I am on the `payments/create/` page with an empty client combo box, **When** I select a client and complete the payment form, **Then** the payment is created successfully

---

### Edge Cases

- What happens when the client ID in the URL is invalid or the client does not exist? The system should handle this gracefully — either show an error or redirect appropriately
- What happens if the user navigates to `payments/create/` with an explicit but invalid `client_id` query parameter? The system should either ignore the invalid parameter or show an appropriate error message
- What happens when the **Nueva Reserva** button is not present on the page? The **New Payment** button should still be placed at the same logical position (rightmost of the action buttons)

## Requirements

### Functional Requirements

- **FR-001**: The system MUST display a **New Payment** button on the `clients/{client_id}/` detail page
- **FR-002**: The **New Payment** button MUST be positioned immediately to the right of the **Nueva Reserva** button
- **FR-003**: Clicking the **New Payment** button MUST navigate the user to the `payments/create/` URL with the current client preselected
- **FR-004**: The client preselection on `payments/create/` MUST use the `client_id` from the referring client detail page
- **FR-005**: When `payments/create/` is accessed directly (not via the **New Payment** button), the client combo box MUST be empty with no preselected client
- **FR-006**: The **New Payment** button text MUST use the existing i18n system and display in Spanish
- **FR-007**: The **New Payment** button MUST be visually styled consistently with the other action buttons on the page (e.g., **Nueva Reserva**, **Edit**)

### Key Entities

- **Client**: The customer record whose detail page contains the **New Payment** button; its ID is used to preselect the client on the payment creation page
- **Payment**: The payment record created via the `payments/create/` page (existing functionality)
- **Client Combo Box**: The selection control on the payment creation page that lists available clients

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can navigate from a client detail page to the payment creation page with the client preselected in 1 click
- **SC-002**: The **New Payment** button is consistently visible on every client detail page that displays action buttons
- **SC-003**: Direct access to `payments/create/` continues to work without regression (client combo box is empty)
- **SC-004**: All button labels are displayed in Spanish using the existing i18n asset system
- **SC-005**: Button placement follows the existing UI pattern — to the right of **Nueva Reserva** — maintaining visual consistency

## Assumptions

- The existing `payments/create/` page already has a client combo box and can accept preselected values via URL parameter or similar mechanism
- The `clients/{client_id}/` detail page already renders action buttons with a consistent layout
- The **Nueva Reserva** button already exists on the page and is used as the positional reference
- The existing i18n system supports Spanish translations for new UI text assets
- The **New Payment** button is within the scope of the existing action button bar, not a separate page section
