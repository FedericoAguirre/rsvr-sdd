# Feature Specification: Duplicated Reservation Alert

**Feature Branch**: `026-duplicated-reservation-alert`

**Created**: 2026-06-29

**Status**: Draft

**Input**: User description: "As an operator I want to receive an alert message, when trying to reserve an already reserved equipment in the same class slot and date."

## Clarifications

### Session 2026-06-29

- Q: When does the duplicate check trigger? → A: Check on equipment addition AND on form submission (double validation).
- Q: What is explicitly out of scope? → A: Out of scope: editing existing reservations, bulk import, and cancellation workflows. Alert applies only to creating reservations.
- Q: How should concurrent conflicts be handled? → A: Check on submit against current DB state (second submitter gets an error). No real-time locking.
- Q: Should duplicate attempts be logged? → A: No logging. The alert is purely a UX improvement.
- Q: What happens when the duplicate check itself fails? → A: Allow the equipment addition but show a non-blocking warning that the check could not be completed (fail open with warning).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operator sees visible duplicate alert on reservation form (Priority: P1)

An operator is creating a reservation and adds an equipment item that is already reserved for the same class slot and date. Instead of the system silently ignoring the duplicate, the operator sees a clear alert message explaining why the equipment cannot be added.

**Why this priority**: This is the core problem — the system currently prevents duplication silently, causing confusion. Making the alert visible is the primary value of this feature.

**Independent Test**: Can be tested by creating a reservation with a duplicate equipment for the same class slot and date, then verifying an alert message is displayed with the date, class slot, and equipment marked as UNAVAILABLE.

**Acceptance Scenarios**:

1. **Given** an operator is on the reservations/create/ page, **When** they attempt to add an equipment item that already has a RESERVED status for the same class slot and date, **Then** a visible alert message is displayed immediately and the duplicate is not added.
2. **Given** a reservation form with a previously undetected duplicate (e.g., reservation state changed after equipment was added), **When** the operator attempts to submit the form, **Then** the duplicate check re-runs and an alert is displayed blocking submission.
3. **Given** an operator sees a duplicate alert, **When** they review the alert content, **Then** the alert includes the date, class slot, and equipment identification marked as UNAVAILABLE.
4. **Given** a reservation form with one duplicated equipment and other non-duplicated equipment, **When** the operator attempts to submit, **Then** the form is not submitted and the alert identifies the conflicting equipment.

---

### User Story 2 - Alert is properly translated to Spanish (Priority: P2)

Spanish-speaking operators see the alert message and its content in Spanish, consistent with the rest of the application's internationalization.

**Why this priority**: The application supports Spanish-speaking operators. The alert must be understandable to all users.

**Independent Test**: Can be tested by switching the application to Spanish locale and verifying the alert message and all its content appear in Spanish.

**Acceptance Scenarios**:

1. **Given** the application is set to Spanish locale, **When** a duplicate equipment alert is triggered, **Then** the alert title, body, date, class slot, equipment label, and "UNAVAILABLE" marker are displayed in Spanish.
2. **Given** the application is set to English locale, **When** a duplicate equipment alert is triggered, **Then** the same content is displayed in English.

---

### User Story 3 - Alert follows accessible UX patterns (Priority: P3)

The alert is designed following UX best practices: visually distinguishable, dismissible, accessible via screen readers, and clearly communicates the problem and the affected data.

**Why this priority**: The alert must be effective for all operators, including those using assistive technologies. Good UX reduces errors and support requests.

**Independent Test**: Can be tested by triggering the duplicate alert and verifying it meets accessibility and readability criteria.

**Acceptance Scenarios**:

1. **Given** a duplicate alert is displayed, **When** inspected, **Then** it has appropriate ARIA roles/labels for screen readers.
2. **Given** a duplicate alert is displayed, **When** the operator interacts with it, **Then** the alert can be dismissed and does not permanently block the form.
3. **Given** multiple duplicate equipment items in a single reservation, **When** the alert is shown, **Then** all conflicting items are listed in the same alert.

---

### Edge Cases

- What happens when the operator removes the duplicated equipment from the reservation and the conflict is resolved? The alert should disappear or update to reflect the current state.
- How does the system handle equipment that was reserved but its status changed to CANCELLED or CHECKED_OUT? Only RESERVED status triggers the duplicate alert.
- What happens when all equipment items in the reservation form are duplicated? The form cannot be submitted, and the alert lists all conflicts.
- How does the alert behave on mobile or narrow viewports? The alert should be responsive and readable at all screen sizes.
- What happens if the operator refreshes the page after seeing the alert? The alert should re-evaluate based on the current form state.
- What happens if the duplicate check cannot be completed (DB timeout, network error)? The equipment addition is allowed and a non-blocking warning is shown: "Could not verify duplicate status."
- What happens if two operators simultaneously reserve the same equipment? The server-side check on form submission catches the conflict; the second submitter sees an error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST detect duplicate equipment conflicts both when an operator adds an equipment item to the reservation AND when the operator attempts to submit the form.
- **FR-002**: System MUST display a visible alert message on the reservations/create/ page when a duplicate equipment is detected.
- **FR-003**: The alert message MUST include: the date, the class slot identifier, and the equipment identifier marked as "UNAVAILABLE" (or its Spanish equivalent).
- **FR-004**: System MUST block form submission while any equipment in the reservation is a duplicate.
- **FR-005**: System MUST remove or update the alert when the conflicting equipment is removed from the reservation.
- **FR-006**: All alert text MUST be i18n-compatible, with translations for Spanish locale.
- **FR-007**: The alert MUST be accessible via keyboard navigation and announced by screen readers.
- **FR-008**: System MUST NOT treat equipment with status other than RESERVED (e.g., CANCELLED, CHECKED_OUT) as duplicates for alert purposes.
- **FR-009**: The alert MUST support listing multiple conflicting equipment items in a single message when more than one duplicate exists.
- **FR-010**: System MUST persist the check against current reservation data (not stale/cached data) to ensure accuracy.
- **FR-011**: If the duplicate check cannot be completed due to system error, the equipment MUST still be added and a non-blocking warning message MUST be displayed indicating the check could not be completed.

### Key Entities *(include if feature involves data)*

- **Reservation**: The reservation being created or edited. Contains equipment items, class slot, and date.
- **Equipment**: The physical item being reserved. Identified by name, code, or other unique identifier.
- **Class Slot**: The time slot for which the reservation is being made (e.g., morning, afternoon, specific hour).
- **Alert Message**: The user-facing notification displayed on the form. Contains date, class slot, and equipment information.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can immediately identify duplicate equipment conflicts — the alert is visible within 1 second of attempting to add a duplicate.
- **SC-002**: Alert message achieves 100% accuracy — no false positives (equipment incorrectly flagged as duplicate) and no false negatives (duplicate not flagged).
- **SC-003**: Form submission is blocked when duplicates exist, and allowed without restriction when all equipment is non-duplicate.
- **SC-004**: Operators report reduced confusion about duplicate equipment in user feedback — support questions about silent duplicate prevention are eliminated.

## Assumptions

- The existing reservation system already has logic to detect duplicate equipment in the same class slot and date — this feature only adds the visible alert layer.
- The application's i18n infrastructure already supports Spanish translations for UI text.
- The equipment identifier displayed in the alert is the same identifier used throughout the application (e.g., equipment name or code).
- The reservation form is a single-page form where equipment can be added/removed before submission.
- Operators use both desktop and mobile browsers to access the reservation form.
- Out of scope: duplicate alert for editing existing reservations, bulk equipment import, and reservation cancellation workflows.
- Duplicate attempt logging is out of scope — no audit trail of rejected duplicates will be persisted.
