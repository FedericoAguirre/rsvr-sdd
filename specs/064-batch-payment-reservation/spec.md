# Feature Specification: Batch Payment-Day Reservations

**Feature Branch**: `064-batch-payment-reservation`
**Created**: 2026-08-11
**Status**: Draft
**Input**: User description: "As a system operator, I want to make batch reservations for the payment day, including available classes that have not started yet, while preserving existing batch reservation rules."

## Clarifications

### Session 2026-08-11

- Q: Should the batch reservation window start on the payment date when an upcoming class remains, and end exactly 20 calendar days after that start date? → A: Start on the payment date if an upcoming slot remains; otherwise start next day; end 20 calendar days later.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reserve eligible classes on payment day (Priority: P1)

As a system operator, I want a batch payment for multiple classes to include available class slots later on the payment day, so the client can attend the next available class instead of waiting for the following week.

**Why this priority**: This is the requested business outcome and changes which classes are immediately available after payment.

**Independent Test**: Create a batch payment at each stated boundary time and verify that the reservation choices include exactly the eligible remaining slots for that day and the applicable lookahead period.

**Acceptance Scenarios**:

1. **Given** the date and time is August 11, 2026 at 17:00 and Tuesday classes at 19:15 and 20:15 are available, **When** the operator pays for five classes, **Then** both Tuesday slots are shown from August 11 through August 31, 2026.
2. **Given** the date and time is August 11, 2026 at 19:00 and both Tuesday classes are available, **When** the operator pays for five classes, **Then** both Tuesday slots are shown from August 11 through August 31, 2026.
3. **Given** the date and time is August 11, 2026 at 19:20 and the 19:15 class has started while the 20:15 class has not, **When** the operator pays for five classes, **Then** only the 20:15 class is shown for August 11 and eligible slots continue through August 31, 2026.
4. **Given** the date and time is August 11, 2026 at 20:20 and all Tuesday classes have started, **When** the operator pays for five classes, **Then** the choices begin on Wednesday, August 12, and include Wednesday 19:15 and 20:15 slots through September 1, 2026.

---

### User Story 2 - Preserve batch reservation rules (Priority: P2)

As a system operator, I want existing batch reservation limits and eligibility rules to continue applying, so including payment-day classes does not create reservations that were previously invalid.

**Why this priority**: Existing operational and capacity rules must remain reliable while the eligible date range changes.

**Independent Test**: Compare batch reservations created before and after the change for the same client, class capacity, payment quantity, and eligibility conditions; only the payment-day start boundary should differ.

**Acceptance Scenarios**:

1. **Given** a slot is unavailable or an existing batch rule excludes it, **When** the operator creates a batch payment, **Then** that slot is not offered.
2. **Given** fewer eligible slots exist than the paid class quantity, **When** the operator creates a batch payment, **Then** the system retains the existing behavior for insufficient availability and does not exceed capacity.

### Edge Cases

- A class is eligible only when its scheduled start time is later than the payment time; a class whose start time is at or before payment is excluded.
- If no eligible class remains on the payment day, the reservation window starts on the next date with eligible availability and ends 20 calendar days after that start date.
- Unavailable, full, cancelled, or otherwise ineligible slots remain excluded according to existing rules.
- If the requested quantity cannot be satisfied within the existing reservation window, the system preserves the current insufficient-availability behavior.
- The payment-day boundary uses the business schedule's configured time zone consistently.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow an operator to create a batch reservation associated with the classes purchased in a payment.
- **FR-002**: The system MUST include available class slots on the payment date when their scheduled start time is later than the payment time.
- **FR-003**: The system MUST exclude payment-day class slots whose scheduled start time is at or before the payment time.
- **FR-004**: When no eligible slot remains on the payment date, the system MUST begin the selectable range on the next date with eligible availability.
- **FR-005**: The system MUST apply existing batch reservation rules for quantity, eligibility, availability, capacity, and date range without relaxation.
- **FR-006**: The system MUST end the reservation window 20 calendar days after its first eligible date, whether that first date is the payment date or the following date.
- **FR-007**: The system MUST support the five-class payment scenario and all other existing supported batch quantities without changing their reservation rules.
- **FR-008**: The system MUST use the configured business schedule time zone when comparing payment time with class start time.

### Key Entities

- **Payment**: The transaction that establishes the reservation start date and time and the number of classes purchased.
- **Class slot**: A scheduled class occurrence with a date, start time, capacity, availability, and eligibility status.
- **Batch reservation**: The group of class reservations associated with one payment and governed by existing batch rules.
- **Reservation window**: The date interval in which eligible class slots may be selected for the payment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In all four stated payment-time scenarios, the displayed eligible slots match the expected inclusion or exclusion of payment-day classes with 100% accuracy.
- **SC-002**: An operator can complete a five-class batch reservation using the displayed eligible slots without waiting for the next weekly schedule.
- **SC-003**: Existing batch reservation regression tests continue to pass, and no reservation exceeds class capacity or existing eligibility rules.
- **SC-004**: The eligible slot list is displayed within 2 seconds for at least 95% of normal reservation attempts.
- **SC-005**: At least 95% of operators can identify the first eligible class and reservation end date without assistance during acceptance testing.

## Assumptions

- The payment timestamp and class start timestamp are evaluated in the configured business schedule time zone.
- The reservation window begins on the payment date when at least one class slot has not started; otherwise it begins on the following date with eligible availability, and ends 20 calendar days after its first eligible date.
- The examples' class availability, capacity, and recurring schedule already exist in the system.
- The feature applies to operator-created batch reservations and does not change client self-service reservation behavior.
- Existing messaging for insufficient availability, full classes, and invalid reservations remains in use.
