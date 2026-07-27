# Feature Specification: Batch Reservations from Payment

**Feature Branch**: `048-batch-reservations-payment`

**Created**: 2026-07-20

**Status**: Draft

**Input**: User description from `ai/features/todos/15-batch-reservations-payment.md`

## Clarifications

### Session 2026-07-20

- Q: Is the date range anchored to "today" or "payment date"? → A: Payment date IS today. Range starts from the next Monday after payment date.
- Q: Does the class slot's day-of-week have to match the selected dates? → A: Yes. If selecting a "Lunes 19:15" slot, the system maps it to the corresponding weekday slot for each date (Lunes slot → Monday, Martes slot → Tuesday, etc.), all at the same hour.
- Q: Must the number of selected dates exactly equal block class count? → A: Yes. The operator selects exactly N dates where N = block class count (≤ 20).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Create Batch Reservations After Payment (Priority: P1)

A system operator completes a payment and immediately creates multiple reservations for that payment in a single batch workflow, without navigating away from the payment flow.

**Why this priority**: This is the core flow that delivers the primary value — eliminating the manual one-by-one reservation creation.

**Independent Test**: Can be tested by creating a payment with N block classes, verifying the batch modal appears, selecting equipment/days/slot, and confirming N reservations are created and linked to the payment.

**Acceptance Scenarios**:

1. **Given** I have just created a payment successfully on the payments creation page, **When** the payment is saved, **Then** a modal for batch reservation creation appears automatically.
2. **Given** the batch modal is open, **When** I view it, **Then** it shows a calendar, an "in service" equipment list, and available hour slots.
3. **Given** I am in the batch modal, **When** I select equipment, an hour slot, and a set of days, **Then** reservations are created and automatically associated to the current payment.
4. **Given** batch reservations were created, **When** I close the modal, **Then** I am redirected to the payment detail page showing all associated reservations.

### User Story 2 — Batch Size & Date Constraints (Priority: P1)

The system enforces limits on batch reservation creation to prevent misuse and data integrity issues.

**Why this priority**: Constraints protect system stability and data consistency.

**Independent Test**: Can be tested by attempting to create batches that exceed limits.

**Acceptance Scenarios**:

1. **Given** I am creating batch reservations, **When** the total would exceed 20 reservations, **Then** the system prevents creation or shows a warning.
2. **Given** I am creating batch reservations, **When** the selected date range exceeds 4 weeks from the payment date, **Then** the system prevents creation.
3. **Given** I am in the batch modal, **When** I select days, **Then** only dates from the next Monday after the payment date up to 4 weeks forward are available.
4. **Given** a conflict exists (equipment + class slot + date already reserved), **When** I attempt to create, **Then** the system handles the unique constraint gracefully with a clear message.

### Edge Cases

- What if all selected dates conflict with existing reservations? The batch should partially fail with clear feedback on which dates could not be created.
- What if the payment's block class number is zero? The batch modal should not appear (no reservations needed).
- What if equipment becomes unavailable after the modal opens? The equipment list should reflect current "in service" status.
- What if the user closes the modal without creating any reservations? The operator is still redirected to the payment detail page (no orphan state).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a modal for batch reservation creation immediately after a payment is saved successfully.
- **FR-002**: The batch modal MUST show a calendar for day selection, an equipment list filtered to "in service" only, and available active class hour slots.
- **FR-003**: System MUST limit available dates from the next Monday after the payment date (start) up to 4 weeks forward (end).
- **FR-004**: System MUST require the operator to select exactly N dates from the available range, where N equals the payment's block class count (N ≤ 20). Only dates whose day-of-week matches the selected class slot's day-of-week are available for selection.
- **FR-005**: System MUST allow the operator to select one piece of equipment from the "in service" list.
- **FR-006**: System MUST allow the operator to select one class hour slot from available active slots.
- **FR-007**: System MUST enforce a maximum of 20 reservations per batch.
- **FR-008**: System MUST enforce that the batch does not exceed a 4-week date range from the payment date.
- **FR-009**: The operator MUST select exactly N dates (one per reservation), where N equals the payment's block class count. The UI enforces this by requiring N date selections before submission.
- **FR-010**: Each created reservation MUST be linked to the payment via a payment-reservation association.
- **FR-011**: Each reservation MUST respect the unique constraint (equipment + class slot + date).
- **FR-012**: Each payment-reservation association MUST be unique (one reservation linked to at most one payment).
- **FR-013**: System MUST display dates in the format 'L - YYYY/MM/DD', 'M - YYYY/MM/DD', etc. (Spanish day abbreviations).
- **FR-014**: The class slot determines the hour (e.g., 19:15) and its day-of-week maps to the corresponding weekday of the selected date. For example, selecting "Lunes 19:15" and dates Mon–Fri creates reservations with "Lunes 19:15" on Monday, "Martes 19:15" on Tuesday, etc. Only dates matching the class slot's weekday are selectable.
- **FR-015**: After closing the batch modal, the system MUST redirect to the payment detail page showing all associated reservations.

### Key Entities *(include if feature involves data)*

- **Payment**: A record of a payment transaction with a block class count.
- **Reservation**: A booking record linking a client, equipment, class slot, and date.
- **PaymentReservation**: A join entity linking a reservation to a payment (unique reservation constraint).
- **Equipment**: A physical item available for reservation, filtered by "in service" status.
- **Class Slot**: A scheduled time slot with a day-of-week, start time, and active status.
- **Batch Reservation**: A transient operation that creates multiple reservation records in one action, associated with a single payment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can create up to 20 reservations in a single batch operation.
- **SC-002**: Batch creation completes and redirects to payment detail within 5 seconds of submission.
- **SC-003**: Zero reservations created outside the allowed date range or exceeding batch limits.
- **SC-004**: All reservations created in a batch are visible on the payment detail page.
- **SC-005**: No orphan reservations exist (every batch reservation is linked to exactly one payment).
- **SC-006**: Unique constraint violations are communicated to the operator with clear, actionable messages.

## Assumptions

- The payments creation page exists and a payment can be saved successfully before the batch modal triggers.
- The payment has a "block class count" field that determines the number of reservations needed.
- Equipment has an "in service" status field for filtering.
- Class slots have an active/inactive status and a day-of-week mapping.
- The payment date IS the current date ("today"). The date range starts from the next Monday after the payment date.
- The operator must select exactly N dates where N equals block class count; the UI enforces this constraint.
- Spanish day abbreviations are used: L (Monday), M (Tuesday), X (Wednesday), J (Thursday), V (Friday), S (Saturday), D (Sunday).
- The batch modal is a one-time operation after payment creation — once closed, it cannot be reopened from the same payment creation flow.
- Conflicts on unique constraints (equipment + class slot + date) result in a partial failure with feedback, not a full batch rollback.
