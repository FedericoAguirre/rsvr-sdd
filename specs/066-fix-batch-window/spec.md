# Feature Specification: Restore 20-Day Batch Reservation Window

**Feature Branch**: `066-fix-batch-window`

**Created**: 2026-08-11

**Status**: Draft

**Input**: For payment `CASH20260811AC003`, the associated batch-reservation modal showed only 15 days ahead instead of the 20 days defined in previous requirements. Restore the full 20-day selection window and verify it against the deployed behavior when available.

## User Scenarios & Testing

### User Story 1 - Show the Full 20-Day Selection Window (Priority: P1)

As a staff user creating batch reservations from a payment, I want the modal to show 20 selectable eligible weekdays so that I can schedule the complete purchased period without losing days to the weekend display filter.

**Why this priority**: Showing only 15 selectable weekdays prevents operators from using the full reservation period defined by the business requirement.

**Independent Test**: Open the batch modal for a payment whose active schedule has five weekday class days and count the selectable date buttons from the first eligible date; exactly 20 must be available when no dates are already reserved.

**Acceptance Scenarios**:

1. **Given** a batch window starts on a Monday and active class days are Monday through Friday, **When** the modal loads, **Then** it displays 20 selectable weekday dates across four complete calendar weeks.
2. **Given** a batch window starts midweek, **When** the modal loads, **Then** it displays 20 selectable weekday dates beginning at the calculated start date and continuing chronologically across the required calendar weeks.
3. **Given** payment `CASH20260811AC003` and its associated reservations are loaded in the deployed environment, **When** the operator opens the batch modal, **Then** the selectable date range contains 20 eligible weekdays rather than the observed 15.

### User Story 2 - Preserve Start-Date and Reservation Rules (Priority: P1)

As a staff user, I want the window extension to preserve the existing payment-day start-date rules and reservation validation so that only the window length changes.

**Why this priority**: Extending the window must not make already-started, unavailable, duplicate, or conflicting reservations valid.

**Independent Test**: Exercise payment-day cutoff, latest-reservation, duplicate-date, unavailable-slot, and outside-window scenarios while asserting the same start-date and validation outcomes as before.

**Acceptance Scenarios**:

1. **Given** an eligible class remains on the payment date, **When** the batch window is calculated, **Then** the window starts on the payment date and exposes 20 eligible weekdays from that start.
2. **Given** no eligible class remains on the payment date, **When** the batch window is calculated, **Then** it starts on the next eligible date and exposes 20 eligible weekdays from that start.
3. **Given** a client has an existing reservation after the payment date, **When** the batch window is calculated, **Then** it starts after the latest reservation according to existing rules and still exposes 20 eligible weekdays.
4. **Given** a user selects a date outside the extended window or selects an unavailable class slot, **When** the batch is submitted, **Then** the existing actionable validation rejects the selection.

### Edge Cases

- Weekends must not reduce the count of selectable eligible weekdays below 20.
- A window beginning Tuesday through Friday must still contain exactly 20 eligible weekdays and preserve weekday-column alignment.
- Reserved dates omitted from the selector must not be replaced by dates outside the calculated window or silently change the business start date.
- Month and year boundaries must not change the count or chronological order of eligible dates.
- If fewer than 20 eligible weekdays exist because of schedule availability, the system must retain its existing insufficient-availability behavior and must not fabricate class dates.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST expose 20 selectable eligible weekdays in the batch reservation modal when at least 20 eligible weekdays are available from the calculated start date.
- **FR-002**: The system MUST extend the date interval far enough to include 20 eligible weekdays instead of limiting the interval to 20 calendar days that render as only 15 weekdays.
- **FR-003**: The system MUST preserve the existing start-date priority and payment-day cutoff rules.
- **FR-004**: The system MUST preserve weekday-column alignment and chronological ordering across the extended interval.
- **FR-005**: The system MUST submit the exact selected dates without shifting them or changing their class weekday.
- **FR-006**: The system MUST preserve existing reservation, availability, duplicate, conflict, permission, and class-slot validation rules.
- **FR-007**: The system MUST use the configured business timezone for determining the first eligible date and calculating the window.
- **FR-008**: The system MUST provide actionable feedback when fewer than 20 eligible weekdays are available or a submitted date is invalid.

### Key Entities

- **Payment**: The payment that determines the initial reservation date and purchased class quantity.
- **Reservation**: Existing or newly selected client attendance on an exact calendar date and class slot.
- **Class slot**: An active weekday/time schedule used to determine whether a date is eligible.
- **Batch reservation window**: The inclusive calendar interval containing the first eligible date and enough eligible weekdays to satisfy the 20-day requirement.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of eligible batch-modal scenarios with at least 20 available weekdays display exactly 20 selectable date buttons.
- **SC-002**: Payment `CASH20260811AC003` displays 20 eligible weekdays in the deployment verification scenario instead of 15.
- **SC-003**: 100% of tested windows beginning on Monday through Friday preserve chronological order and weekday-column alignment.
- **SC-004**: Existing payment-day, conflict, duplicate, unavailable-slot, and outside-window tests continue to pass without changed rejection behavior.
- **SC-005**: Operators can complete a 20-date selection without manually compensating for weekends or using dates outside the displayed window.

## Assumptions

- The requirement of “20 days” means 20 selectable eligible weekdays, because the modal intentionally omits weekends and the observed 20-calendar-day interval produced only 15 visible weekdays.
- The existing start date, active weekday schedule, and payment-day cutoff rules remain unchanged.
- The current payment identifier and associated reservations are available in the deployment environment used for verification; deployment data is not modified by this feature.
- The existing five-weekday modal columns remain the user-facing calendar structure.
- If the schedule cannot provide 20 eligible weekdays, existing insufficient-availability behavior remains authoritative.
- No new payment configuration or database entity is required.

## Clarifications

No critical ambiguities detected. The observed 15-versus-20 discrepancy and the existing weekday-only modal make the required interpretation explicit: extend the calendar interval until 20 selectable eligible weekdays are available.
