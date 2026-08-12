# Feature Specification: Batch Reservation Date Alignment

**Feature Branch**: `065-batch-reservation-date-alignment`

**Created**: 2026-08-11

**Status**: Draft

**Input**: Correct batch reservation date alignment with weekday columns and prioritize the default payment day, selected payment date, or next day after the latest reservation.

## User Scenarios & Testing

### User Story 1 - Select Aligned Batch Dates (Priority: P1)

As a staff user recording a payment, I want batch reservation dates to appear under the correct weekday columns so that I can select dates without confusing a calendar date with another weekday.

**Why this priority**: Incorrect weekday alignment can cause reservations to be created on unintended days and directly undermines the primary batch-reservation workflow.

**Independent Test**: Open the batch reservation date selector for payments with active class days across multiple weekdays and verify every displayed date appears in the column matching its calendar weekday.

**Acceptance Scenarios**:

1. **Given** active class days span multiple weekdays, **When** the batch reservation selector opens, **Then** each displayed date is placed under the column for that date's actual weekday.
2. **Given** a date is displayed in a weekday column, **When** the user selects it, **Then** the selected reservation uses that same calendar date without shifting it to another weekday.

### User Story 2 - Choose the Correct Starting Date (Priority: P1)

As a staff user, I want the date list to begin from the correct starting point so that the batch reservation period reflects the payment cycle and the client's existing reservations.

**Why this priority**: The starting date determines the entire batch period and prevents missed or duplicate reservation days.

**Independent Test**: Exercise the selector with payment dates and existing reservations representing each priority case, then compare the first displayed date with the expected date.

**Acceptance Scenarios**:

1. **Given** a valid default payment day is available, **When** the date period is calculated, **Then** the period starts on that default payment day.
2. **Given** no usable default payment day is available and the selected payment date is valid, **When** the date period is calculated, **Then** the period starts on the selected payment date.
3. **Given** the selected payment date cannot be used because a later reservation already exists, **When** the date period is calculated, **Then** the period starts on the day after the latest reservation.

### User Story 3 - Preserve Existing Batch Behavior (Priority: P2)

As a staff user, I want existing batch reservation validation and selection behavior to remain intact while dates are realigned so that the correction does not introduce unrelated changes.

**Why this priority**: Alignment is a correction to date presentation and calculation, not a change to reservation ownership, conflict, or authorization rules.

**Independent Test**: Run existing batch reservation scenarios for conflicts, unavailable dates, and chronological ordering after alignment is applied.

**Acceptance Scenarios**:

1. **Given** a selected date is outside the valid batch period, **When** the user submits the batch reservation, **Then** the system rejects it with the existing actionable validation behavior.
2. **Given** valid dates are selected in chronological order, **When** the user submits the batch reservation, **Then** reservations are created for those exact dates in that order.

### Edge Cases

- If no active class days exist, the selector must not fabricate weekday options or shift dates to an arbitrary weekday.
- If the default payment day, selected payment date, and day after the latest reservation produce different candidates, the priority order must be applied deterministically.
- Dates crossing a month or year boundary must remain valid and retain their actual weekday placement.
- A payment date that is already represented by a later reservation must not create a duplicate starting date.
- Empty, unavailable, or conflicting date selections must retain the existing user-facing validation behavior.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST calculate the batch reservation start date using this priority order: default payment day when available, selected payment date when valid, then the day after the latest existing reservation as fallback.
- **FR-002**: The system MUST preserve the calculated start date's actual calendar weekday when generating the batch reservation date period.
- **FR-003**: The date selector MUST place every displayed date under the weekday column corresponding to that date's calendar weekday.
- **FR-004**: The system MUST preserve chronological ordering of all generated batch reservation dates across month and year boundaries.
- **FR-005**: The system MUST submit the exact dates selected by the user without changing their weekday or calendar date.
- **FR-006**: The system MUST preserve existing validation for unavailable dates, duplicate reservations, conflicts, permissions, and invalid date ranges.
- **FR-007**: The system MUST provide actionable user-facing feedback when no valid batch reservation date can be selected.

### Key Entities

- **Payment**: The payment event that supplies the default or selected payment date used to calculate the batch period.
- **Reservation**: An existing or newly selected client reservation with a calendar date and weekday.
- **Class day**: An active weekday on which reservations may be selected and displayed in the date selector.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of dates displayed in the batch selector appear under the column matching their calendar weekday in automated acceptance scenarios.
- **SC-002**: 100% of valid starting-date scenarios select the first date according to the documented priority order.
- **SC-003**: 100% of selected valid dates are submitted unchanged, including dates crossing month or year boundaries.
- **SC-004**: Existing batch reservation acceptance scenarios continue to pass with no increase in duplicate, conflict, or invalid-date outcomes.
- **SC-005**: A staff user can identify the weekday for every displayed date without consulting an external calendar.

## Assumptions

- The default payment day is the payment date already used by the existing batch reservation workflow; no new payment-day configuration is introduced by this feature.
- Existing weekday column labels and the current batch reservation modal remain the user-facing calendar structure.
- Existing reservation, class availability, permission, and conflict rules remain authoritative.
- Date calculations use the project's configured business timezone.
- Mobile and desktop layouts are both expected to preserve weekday-to-date alignment, but no visual redesign is required.

## Clarifications

No critical ambiguities detected worth formal clarification. The stated priority order and existing batch reservation concepts provide sufficient scope for planning.
