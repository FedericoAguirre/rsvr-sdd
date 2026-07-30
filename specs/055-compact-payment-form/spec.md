# Feature Specification: Compact Payment Form Layout for Single-Screen View

**Feature Branch**: `055-compact-payment-form`

**Created**: 2026-07-30

**Status**: Draft

**Input**: User description: "Redesign the payment creation form (`/payments/create/`) to fit all fields and buttons on a single screen without scrolling, improving usability and reducing friction during data entry."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Payment Without Scrolling (Priority: P1)

As a staff user creating a payment on `/payments/create/`, I want all form fields and action buttons to fit on a single screen so that I can enter payments quickly without scrolling to find hidden fields or the submit button.

**Why this priority**: This is the primary workflow — every payment entry session benefits from reduced scrolling, and the submit button remaining visible eliminates uncertainty about form completion.

**Independent Test**: Can be fully tested by opening `/payments/create/` on a 1080p display and verifying no vertical scrolling is needed to see all fields and buttons.

**Acceptance Scenarios**:

1. **Given** I open the payment creation form on a 1080p display, **When** the page loads, **Then** all fields, help text triggers, and action buttons are visible without vertical scrolling.
2. **Given** I focus on a field with help text, **When** the field receives focus, **Then** the help text appears below the field.
3. **Given** I submit the form with valid data, **When** I click the submit button, **Then** the payment is created successfully (same behavior as before).

---

### User Story 2 - Edit a Payment With Compact Layout (Priority: P2)

As a staff user editing an existing payment, I want the edit form to also fit on a single screen so that I can review and update all fields at a glance.

**Why this priority**: Editing is a secondary but common workflow — consistency between create and edit modes reduces cognitive load.

**Independent Test**: Can be fully tested by opening an existing payment's edit page and verifying all fields fit without scrolling.

**Acceptance Scenarios**:

1. **Given** I open the payment edit form on a 1080p display, **When** the page loads, **Then** all fields and buttons are visible without vertical scrolling.
2. **Given** I save changes on the compact edit form, **When** I click "Save Changes", **Then** the payment is updated successfully.

---

### User Story 3 - Use Form on Smaller Screens (Priority: P3)

As a staff user accessing the payment form on a tablet or mobile device, I want the form to remain usable with fields stacked vertically so that I can still enter payments on smaller viewports.

**Why this priority**: Mobile usage is less frequent than desktop, but must not regress from the current experience.

**Independent Test**: Can be tested by resizing the browser to tablet (768px) and mobile (375px) widths and verifying the form stacks vertically with no horizontal scrolling.

**Acceptance Scenarios**:

1. **Given** I open the form on a tablet-width viewport (768px), **When** the page renders, **Then** multi-column layouts stack vertically and the form remains scrollable if needed.
2. **Given** I open the form on a mobile-width viewport (375px), **When** the page renders, **Then** fields appear stacked vertically with full-width buttons and no horizontal overflow.

---

### Edge Cases

- What happens when the browser is zoomed to 110%? All fields should remain visible or the form should scroll naturally without clipping content.
- What happens when a field contains a very long value (e.g., lengthy notes)? The field should not overflow its container; text should wrap or truncate appropriately.
- What happens with the file upload field (Comprobante)? The input should remain functional and properly sized even in the compact layout.
- What happens when validation errors are present? Error messages must display below the relevant field without being cut off or overlapping adjacent fields.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The payment form MUST fit entirely within a 1080p viewport (1920x1080) without requiring vertical scrolling, assuming standard browser chrome.
- **FR-002**: Help text for each field MUST be accessible but hidden by default, appearing on field focus or hover.
- **FR-003**: All form controls, labels, and action buttons MUST remain readable and properly sized for touch interaction (minimum 44x44px touch targets).
- **FR-004**: The form MUST maintain responsive behavior: multi-column layout on desktop (>= 1024px), adjusted layout on tablet (769px–1024px), and vertical stacking on mobile (< 768px).
- **FR-005**: Form submission, validation, error display, and file upload MUST work identically to the current implementation — only visual spacing and sizing changes are permitted.
- **FR-006**: The compact layout MUST apply consistently to both create and edit modes of the payment form.
- **FR-007**: All labels MUST be internationalized via i18n — no hardcoded user-visible strings.

### Key Entities

- **Payment**: The payment record being created or edited. The underlying model and its fields are unchanged — only the form's visual presentation is modified.
- **Payment Form Template**: The Django template rendering the form. This is the primary artifact being modified.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The form height is at most 600px on desktop, fitting entirely within a 1080p viewport without scrolling.
- **SC-002**: No vertical scrolling is required to view all fields and action buttons on displays 1080p and larger at 100% zoom.
- **SC-003**: All fields remain accessible and readable — label text is clearly visible, input controls are adequately sized, and validation errors display without clipping.
- **SC-004**: Help text appears on field focus or hover and disappears when the field loses focus (if empty), keeping the compact layout clean by default.
- **SC-005**: The responsive layout degrades gracefully: multi-column on desktop, adjusted on tablet, and vertical stack on mobile with no horizontal overflow.

## Assumptions

- Standard desktop browser chrome (toolbar, tabs, bookmarks) occupies approximately 200–250px of vertical space on 1080p displays, leaving 600–700px available for content.
- The existing `PaymentForm` class and its field definitions are correct and complete — no fields are being added or removed.
- The existing form validation, submission, and file upload logic is unchanged — only CSS and template markup are modified.
- CSS-only styling changes are sufficient to achieve the target compact layout; no backend Python changes are needed.
- Mobile-first redesign is explicitly out of scope — the current mobile experience is to be maintained as-is, not redesigned.
- All user-visible strings are to remain internationalized via existing i18n mechanisms; no strings are being hardcoded.
