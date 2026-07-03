# Feature Specification: Payments Associate Button

**Feature Branch**: `029-payments-associate-button`

**Created**: 2026-07-02

**Status**: Draft

**Input**: Use the @ai/features/todos/03-Button-access-reservations-payments.md to create the new feature

## User Scenarios & Testing

### User Story 1 - Associate Payment via Button (Priority: P1)

As a system Operator viewing a payment detail page, I want to click an **Associate** button so that I can navigate to the payment association page and link the current payment to a reservation.

**Why this priority**: This is the only user journey — the entire feature is adding this button and ensuring the tab order is consistent.

**Independent Test**: Can be fully tested by navigating to any payment detail page, confirming the Associate button appears to the left of the Edit button, clicking it, and verifying the browser navigates to the association page.

**Acceptance Scenarios**:

1. **Given** I am on the `payments/{payment_id}/` detail page, **When** I view the action buttons, **Then** an **Associate** button is displayed to the left of the **Edit** button
2. **Given** I am on the `payments/{payment_id}/` detail page, **When** I click the **Associate** button, **Then** I am navigated to the `payments/{payment_id}/associate/` page
3. **Given** I am on the `payments/{payment_id}/` detail page, **When** I press the Tab key sequentially through the form controls, **Then** the focus order reaches the Associate button before the Edit button

---

### Edge Cases

- What happens when the payment is already associated? The button should still be present (association page handles re-association or displays current association)
- What happens on a payment that doesn't exist (404)? The detail page is never rendered, so the button is never shown

## Requirements

### Functional Requirements

- **FR-001**: The system MUST display an **Associate** button on the `payments/{payment_id}/` detail page
- **FR-002**: The Associate button MUST be positioned immediately to the left of the **Edit** button
- **FR-003**: Clicking the Associate button MUST navigate the user to the `payments/{payment_id}/associate/` URL
- **FR-004**: The keyboard tab order MUST place the Associate button before the Edit button
- **FR-005**: The Associate button MUST be visually styled consistently with the other action buttons on the page

### Key Entities

- **Payment**: The payment record being viewed; its ID is used to construct the associate URL
- **Payment Association**: The relationship managed via the `payments/{payment_id}/associate/` page (existing functionality)

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator can navigate from any payment detail page to the association page in one click via the Associate button
- **SC-002**: The Associate button is always positioned left of Edit, regardless of screen size or device
- **SC-003**: Keyboard-only users can tab to Associate before Edit in the natural form order
- **SC-004**: The button click navigates to the correct URL (validated across all existing payments)

## Assumptions

- The `payments/{payment_id}/associate/` page already exists and functions correctly
- The existing Edit button remains unchanged in behavior
- The Operator role already has permission to access the association page
- Standard Django/Gunicorn navigation patterns apply (no SPA routing)
- Mobile/responsive layout should preserve the left-of-Edit ordering
