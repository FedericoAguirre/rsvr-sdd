# Feature Specification: Reorder Payment Form Fields for Improved UX

**Feature Branch**: `054-payments-form-reorder`

**Created**: 2026-07-30

**Status**: Draft

**Input**: User description: "Reorder payment form fields on /payments/create/ to follow a logical workflow: client → transaction details → notes/documentation → submit."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enter a Payment with Logical Field Flow (Priority: P1)

As a staff user creating a payment on `/payments/create/`, I want the form fields to follow a natural payment-entry flow (identify client first, then enter transaction details, then documentation) so that I can enter payments quickly without jumping between unrelated fields.

**Why this priority**: This is the only user workflow — every payment creation session benefits from logical field ordering.

**Independent Test**: Can be fully tested by navigating to `/payments/create/` and verifying fields appear in the specified order.

**Acceptance Scenarios**:

1. **Given** I access the payment creation form, **When** the page loads, **Then** fields appear in this order: Cliente, Amount, Cantidad de bloques de clase, Tipo de pago, Fecha, Notas, Identificador de pago, Referencia, Comprobante.
2. **Given** I tab through the form, **When** I press Tab repeatedly, **Then** focus moves through fields in the same logical order as they appear on screen.
3. **Given** I submit the form with valid data in the new field order, **When** I click "Crear pago", **Then** the payment is created successfully and I am redirected to the payment detail page.
4. **Given** the form has validation errors, **When** errors are displayed, **Then** error messages appear below the relevant field regardless of field position.

---

### Edge Cases

- What happens when the form is viewed on mobile? Fields should stack vertically in the same order (responsive layout).
- What happens if a tabbable element (e.g., a select2 dropdown) is used for Cliente? The tab order must still follow the visual field order.
- What happens with file upload for Comprobante at the bottom? It should work as before — field position does not affect file handling.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The payment creation form MUST display fields in the following exact order: Cliente, Amount, Cantidad de bloques de clase, Tipo de pago, Fecha, Notas, Identificador de pago, Referencia, Comprobante.
- **FR-002**: The form submit button ("Crear pago") and cancel button ("Cancelar") MUST appear below all form fields.
- **FR-003**: The form MUST render correctly on desktop (fields grouped logically in rows) and mobile (fields stacked vertically).
- **FR-004**: Form validation and submission MUST work identically regardless of field display order.
- **FR-005**: The Django form field ordering in `Meta.fields` MUST match the visual display order.

### Key Entities

- **Payment**: The payment record being created. Only the form field ordering changes — the underlying model and its fields are unaffected.
- **Client**: The member associated with the payment, selected first in the form.
- All other entities (class blocks, payment types, etc.) are unchanged — only their display position changes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Fields on `/payments/create/` display in the exact order specified in FR-001.
- **SC-002**: Tab order follows the visual field order top-to-bottom.
- **SC-003**: Form submission with valid data creates a payment record successfully (same behavior as before reordering).
- **SC-004**: Form validation errors display below the correct fields.

## Assumptions

- The existing `Payment` model fields are correct and complete — no new fields are being added.
- The existing form validation logic is correct — only the field order is changing.
- The payment form exists at `payments/forms.py` and the template at `templates/payments/create.html`.
- The existing view logic in `payments/views.py` does not need changes for field reordering.
- The form already handles file uploads for Comprobante — no upload logic changes needed.
