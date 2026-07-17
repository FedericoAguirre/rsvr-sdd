# Feature Specification: Update Auto-Date Algorithm

**Feature Branch**: `047-update-date-algorithm`

**Created**: 2026-07-17

**Status**: Draft

**Input**: User description from `ai/features/todos/11-update-date-algorithm.md`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Next-Week Auto-Date (Priority: P1)

When a system user creates a new reservation and selects a class slot, the date field is automatically set to the same day-of-week in the following week. No time-based edge cases or same-week logic apply. If no class slot is selected, the date stays unmodified.

**Why this priority**: This is the core behavior change replacing the previous algorithm.

**Independent Test**: Can be fully tested by loading the reservation create page, selecting a class slot on any day, and verifying the date is always set to the same day-of-week in the following week (e.g., selecting a Monday slot on any day always produces next Monday's date).

**Acceptance Scenarios**:

1. **Given** I am creating a new reservation on any day of the week, **When** I select a class slot, **Then** the date field is set to the same day-of-week in the following week.
2. **Given** I am creating a new reservation with a date auto-filled, **When** I change the class slot to a different day-of-week, **Then** the date recalculates to the new day-of-week in the following week.
3. **Given** I am creating a new reservation with a date auto-filled, **When** I manually modify the date, **Then** the manual value is preserved and subsequent class slot changes do NOT recalculate it.
4. **Given** I am creating a new reservation, **When** no class slot is selected, **Then** the date field remains unmodified.

---

### User Story 2 - Edge Cases (Priority: P2)

The simplified algorithm handles boundary cases cleanly without special time-based logic.

**Why this priority**: Most users won't encounter edge cases daily, but correctness matters.

**Independent Test**: Can be tested by creating reservations at different times and verifying the "next week" rule always applies.

**Acceptance Scenarios**:

1. **Given** today matches the class slot's day-of-week, **When** I select the slot, **Then** the date is set to the same day-of-week next week (not today).
2. **Given** the class slot's day-of-week is a future day later this week, **When** I select the slot, **Then** the date is set to the same day-of-week next week (not this week).
3. **Given** the class slot's day-of-week is a past day this week, **When** I select the slot, **Then** the date is set to the same day-of-week next week.

### Edge Cases

- What happens at midnight exactly (00:00)? Treated as the start of the new day — the auto-date is always the same day-of-week next week regardless of time.
- What if the user changes date after auto-fill, then changes class slot again? The date stays as the user manually set it — it does NOT recalculate.
- What if there are no future occurrences? The "next week" calculation always produces a valid date (same day-of-week, +7 days).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST auto-set the date field when a class slot is selected on the reservation create page.
- **FR-002**: The auto-date MUST always be set to the same day-of-week as the selected class slot, in the following week (today + 7 days if same day-of-week, otherwise next occurrence + crossing into next week).
- **FR-003**: System MUST recalculate the auto-date when the class slot selection changes (unless a manual override is in effect).
- **FR-004**: System MUST allow manual date override after auto-fill.
- **FR-005**: Once a user manually edits the date, subsequent class slot changes MUST NOT recalculate the date.
- **FR-006**: System MUST NOT modify the date field when no class slot is selected.

### Key Entities *(include if feature involves data)*

- **Reservation**: A booking record linking a client to a class slot on a specific date.
- **Class Slot**: A scheduled time slot (with a day-of-week, start time, end time) that can be reserved.
- **Auto-Date Calculation**: The business logic that determines the correct date based on the selected class slot — always the next occurrence of the class slot's day-of-week.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Date field auto-populates within 1 second of class slot selection.
- **SC-002**: Selecting any class slot on any day always produces a date in the following week (not the current week).
- **SC-003**: Manual date overrides are respected and not overwritten by subsequent auto-fill.
- **SC-004**: Zero date-capture errors on reservations created with the auto-date feature.

## Assumptions

- The reservation create page has a class slot dropdown/select input and a date input field.
- Class slots have a day-of-week (0=Monday..6=Sunday), start time, and end time.
- The auto-date logic runs client-side (JavaScript) for immediate feedback, with server-side validation.
- Day-of-week mapping follows ISO standard (Monday=0..Sunday=6).
- The feature is limited to the reservation create page; the edit page is out of scope for v1.
- This replaces the previous algorithm from feature 041 — all time-based same-day rules are removed.
