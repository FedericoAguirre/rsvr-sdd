# Feature Specification: Order Reservations by Date in Payment Detail

**Feature Branch**: `042-order-reservations-date`

**Created**: 2026-07-14

**Status**: Draft

**Input**: User description: "Order reservations by date descending in payment detail"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Payment Reservations Sorted by Date (Priority: P1)

As an operator viewing a payment detail page, I want the associated reservations ordered by date descending (most recent first), so that I can quickly identify the latest reservation without manually scanning the list.

**Why this priority**: This is the only requirement — the entire feature is a single focused change to the reservation list sort order in the payment detail view.

**Independent Test**: Load any payment detail page with multiple reservations on different dates and verify the most recent date appears at the top.

**Acceptance Scenarios**:

1. **Given** I am viewing a payment detail page with reservations on multiple dates, **When** the page loads, **Then** reservations are sorted by date descending (most recent first).

2. **Given** I am viewing a payment detail page with reservations on the same date, **When** the page loads, **Then** same-date reservations are sorted by class slot time descending (latest time first).

3. **Given** I am viewing a payment detail page with no associated reservations, **When** the page loads, **Then** the reservation list is empty (no change in behavior).

---

### Edge Cases

- **No reservations**: Payment detail page with zero associated reservations — list renders empty, no sorting applies.
- **Single reservation**: Only one reservation exists — sorting is a no-op but must not break.
- **All same date**: Multiple reservations all on the same date — secondary sort by class slot time descending applies.
- **Future and past dates mixed**: Reservations span past and future dates — most recent date (which could be in the future) appears first.
- **Same date and time**: Multiple reservations on the same date and class slot — tie-breaking is undefined; any stable order is acceptable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The reservation list on the payment detail page MUST be sorted by reservation date in descending order (most recent first).
- **FR-002**: When multiple reservations share the same date, they MUST be sorted by their associated class slot time in descending order within that date.
- **FR-003**: The sorting behavior MUST NOT alter the displayed data or affect any other page functionality — only the display order changes.

### Key Entities *(include if feature involves data)*

- **Reservation**: Represents a booked class session. Has a date attribute and is associated with a class slot (which has a time). This feature changes only how existing reservations are ordered in the payment detail view.
- **Payment**: Groups multiple reservations together. The payment detail page is the context where the reordered reservation list is displayed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a payment detail page with 3+ reservations on different dates, the most recent reservation appears at the top of the list on every page load.
- **SC-002**: On a payment detail page with 2+ reservations on the same date, reservations are ordered by class slot time descending (latest class first).
- **SC-003**: All existing payment detail page functionality remains unchanged — sorting is the only behavioral difference.
- **SC-004**: Zero regression in payment detail page data accuracy — no reservations are lost, duplicated, or modified.

## Assumptions

- The existing payment detail page and its reservation list component are the only places this change applies.
- The secondary sort field (class slot time) exists and is accessible on each reservation record.
- Reservations without an associated class slot time will fall back to date-only sorting and appear in any order within the same date.
- The change is purely presentational (query-level sort) — no UI or layout changes are required.
