# Feature Specification: Auto-set Date on Class Slot Selection

**Feature Branch**: `041-auto-date-class-slot`

**Created**: 2026-07-13

**Status**: Draft

**Input**: User description from `ai/features/todos/09-reservations-date-class-slot.md`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Auto-Date on Class Slot Select (Priority: P1)

When a system user creates a new reservation and selects a class slot, the date field is automatically set to the closest future occurrence of that class slot's day-of-week, based on specific time rules. If no class slot is selected, the date stays unmodified.

**Why this priority**: This eliminates date capture errors — the core value of the feature.

**Independent Test**: Can be fully tested by loading the reservation create page, selecting a class slot, and verifying the date field updates according to the business rules.

**Acceptance Scenarios**:

1. **Given** I am creating a new reservation, **When** I select a class slot, **Then** the date field is automatically set following the auto-date calculation rules.
2. **Given** I am creating a new reservation with a date auto-filled, **When** I change the class slot, **Then** the date recalculates automatically.
3. **Given** I am creating a new reservation with a date auto-filled, **When** I manually modify the date, **Then** the manual value is preserved.
4. **Given** I am creating a new reservation, **When** no class slot is selected, **Then** the date field remains unmodified.

### User Story 2 - Edge Cases and Time-Boundaries (Priority: P2)

The auto-date logic correctly handles time boundaries: same-day slots before earliest class time, same-day slots after all class times, and cross-week boundaries.

**Why this priority**: Correct time-boundary behavior is critical for reliability but most users won't hit these edge cases daily.

**Independent Test**: Can be tested by creating reservations at different times of day and verifying the date calculation matches the examples table.

**Acceptance Scenarios**:

1. **Given** today is the class slot's day-of-week, **When** the current time is before the earliest class time on that day, **Then** the auto-date skips to next week (all same-day slots are skipped).
2. **Given** today is the class slot's day-of-week, **When** the current time is past any class time on that day, **Then** the auto-date skips to next week.
3. **Given** the class slot's day-of-week is a different future day this week, **When** selected, **Then** the auto-date is set to that day this week.
4. **Given** the class slot's day-of-week is a past day this week, **When** selected, **Then** the auto-date is set to that day next week.

---

### Edge Cases

- What happens at midnight exactly (00:00)? Should be treated as the start of the new day.
- What if the user changes date after auto-fill, then changes class slot again? The date should recalculate from the new class slot, overriding the manual value.
- What if there are no future occurrences (e.g., the last class of the week just ended)? Should be addressed gracefully — maybe fall back to next week.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST auto-set the date field when a class slot is selected on the reservation create page.
- **FR-002**: The auto-date calculation MUST follow: if today matches the class slot's day-of-week and current time is before earliest class time OR past any class time → set to same day next week.
- **FR-003**: The auto-date calculation MUST follow: if the class slot's day-of-week is a different future day this week → set to that day this week.
- **FR-004**: The auto-date calculation MUST follow: if the class slot's day-of-week is a past day this week → set to that day next week.
- **FR-005**: System MUST recalculate the auto-date when the class slot selection changes.
- **FR-006**: System MUST allow manual date override after auto-fill.
- **FR-007**: System MUST NOT modify the date field when no class slot is selected.

### Key Entities *(include if feature involves data)*

- **Reservation**: A booking record linking a client to a class slot on a specific date.
- **Class Slot**: A scheduled time slot (with a day-of-week, start time, end time) that can be reserved.
- **Auto-Date Calculation**: The business logic that determines the correct date based on the selected class slot, the current day/time, and week boundaries.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Date field auto-populates within 1 second of class slot selection.
- **SC-002**: All examples in the specification's examples table produce the correct auto-date.
- **SC-003**: Manual date overrides are respected and not overwritten by subsequent auto-fill.
- **SC-004**: Zero date-capture errors on reservations created with the auto-date feature.

## Assumptions

- The reservation create page has a class slot dropdown/select input and a date input field.
- Class slots have a day-of-week (0=Monday..6=Sunday), start time, and end time.
- "Earliest class time" refers to the earliest start time among all classes scheduled on a given day-of-week.
- "Past any class time" means the current time is after the start time of the class slot being considered.
- The auto-date logic runs client-side (JavaScript) for immediate feedback, with server-side validation.
- Day-of-week mapping follows ISO standard (Monday=0..Sunday=6).
- The feature is limited to the reservation create page; the edit page is out of scope for v1.
