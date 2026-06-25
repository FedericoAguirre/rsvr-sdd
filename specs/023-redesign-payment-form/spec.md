# Feature Specification: Payment Form Redesign

**Feature Branch**: `023-redesign-payment-form`

**Created**: 2026-06-24

**Status**: Draft

**Input**: User description: "Redesign the payments/create/ form to adhere to the django form standards in this project"

## User Scenarios & Testing

### User Story 1 - Operators Use the Standardized Payment Form (Priority: P1)

As an operator, I want the payment creation form to look and behave consistently with other forms in the system (client, equipment, reservation forms) so that I don't have to learn a different layout or deal with misaligned fields.

**Why this priority**: Visual consistency is a core UX requirement. The current payment form uses full-width fields (`col-12`) while every other form uses a two-column grid (`col-md-6`). This inconsistency creates a jarring experience when switching between modules.

**Independent Test**: Can be fully tested by navigating to the payment creation page and visually confirming the grid matches other forms in the system. No functionality changes are needed.

**Acceptance Scenarios**:

1. **Given** I am on the payment creation page, **When** I view the form, **Then** each field is rendered in a `col-md-6` column wrapper, matching the layout of client, equipment, and reservation forms.
2. **Given** I am on the payment creation page, **When** I inspect any input, select, or textarea field, **Then** it has the Bootstrap `form-control` class applied, giving it the same visual style as fields in other forms.
3. **Given** I fill in the form and submit, **When** validation errors occur, **Then** errors appear in `<div class="text-danger">` per field, identical to error display in other forms.
4. **Given** I submit the form with valid data, **When** the payment is saved, **Then** I am redirected to the payment detail page (no change in behavior).
5. **Given** the form includes an evidence image upload field, **When** I view the form, **Then** the file input has `form-control` styling and the form includes `enctype="multipart/form-data"` (existing behavior preserved).

---

### User Story 2 - Developers Maintain Consistent Form Code (Priority: P2)

As a developer, I want the payments form and template to use the same patterns as other forms in the project so that code is predictable, easier to maintain, and less error-prone when making future changes.

**Why this priority**: Code consistency reduces cognitive load during maintenance and lowers the risk of regressions. The current form lacks `form-control` widget attrs and uses an incorrect column class, making it a one-off that could be overlooked during global changes.

**Independent Test**: Can be verified by code review comparing the payments form/template against the client or equipment form/template.

**Acceptance Scenarios**:

1. **Given** I review the `PaymentForm.Meta.widgets` definition, **When** I check each widget, **Then** every widget has `"class": "form-control"` in its attrs, matching the pattern used in `ClientForm`, `EquipmentForm`, and `ReservationForm`.
2. **Given** I review `payment_form.html`, **When** I check the field loop, **Then** field wrappers use `col-md-6` (not `col-12`), matching other form templates.
3. **Given** I review the edit mode, **When** field locking is applied, **Then** locked fields still appear styled with `form-control` (disabled appearance).

---

### Edge Cases

- What happens when an evidence image is uploaded? The file input retains `form-control` styling while keeping the `enctype="multipart/form-data"` form attribute.
- What happens when the form is in edit mode with locked fields? Disabled fields still display the `form-control` class (applied via widget attrs), maintaining visual consistency.
- What happens on mobile viewports? The `col-md-6` class stacks to full-width on small screens (Bootstrap responsive behavior), identical to all other forms.

## Requirements

### Functional Requirements

- **FR-001**: The payment creation template MUST wrap each form field in `<div class="col-md-6">` instead of `<div class="col-12">`, matching the project-wide form layout convention.
- **FR-002**: The button row (`col-12`) MUST remain full-width and be placed last inside the form, unchanged from current behavior.
- **FR-003**: Every widget in `PaymentForm.Meta.widgets` MUST include `"class": "form-control"` in its attrs dictionary, ensuring consistent Bootstrap styling.
- **FR-004**: The `date` widget MUST retain `{"type": "date"}` alongside the new `"class": "form-control"` attribute.
- **FR-005**: The `notes` widget MUST retain `{"rows": 3}` alongside the new `"class": "form-control"` attribute.
- **FR-006**: All existing form behavior MUST be preserved: field locking in edit mode, evidence validation, amount validation, class slot count validation, CSRF token rendering, and help text display.
- **FR-007**: The `enctype="multipart/form-data"` attribute on the `<form>` tag MUST be preserved for evidence image upload.
- **FR-008**: The form MUST continue using manual field iteration (`{% for field in form %}`) rather than `{{ form.as_p }}` or `{{ form.as_div }}`, matching the project standard.

### Key Entities

- **PaymentForm (ModelForm)**: The Django ModelForm class for the Payment model. Currently does not set `form-control` on most widget attrs. After redesign, all widget attrs will include `"class": "form-control"`.
- **payment_form.html**: The template rendering the payment form. Currently uses `col-12` field wrappers. After redesign, field wrappers will use `col-md-6`.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The payment creation form visually matches the client, equipment, and reservation forms in field width, input styling, error display, and button layout.
- **SC-002**: All existing form validation and submission logic continues to work with zero regressions.
- **SC-003**: Code reviewers can confirm that the payments form/template follow the same widget/column patterns as the project's reference forms.
- **SC-004**: No user-facing behavior changes other than the visual grid layout and input styling.

## Assumptions

- The existing `col-12` layout was unintentional or a carryover from an earlier version, not a deliberate design choice for the payments form specifically.
- The evidence file input will benefit from `form-control` styling like all other inputs.
- The project's existing forms (client, equipment, reservation) represent the canonical standard that the payment form should match.
- No changes to the view logic or form validation logic are required — only the template and widget attrs need updating.
