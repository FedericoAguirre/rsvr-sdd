# Feature Specification: Batch Reservation Weekly Date Groups

**Feature Branch**: `056-batch-reservation-weekly-groups`

**Created**: 2026-07-30

**Status**: Draft

**Input**: User description: "Organize the date selection display in the batch reservation modal (`/payments/{id}/?batch_modal=1`) to show 20 dates in logical weekly groups (5 dates per line, Monday-Friday), improving readability and reducing confusion when selecting dates."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Dates Grouped by Week (Priority: P1)

As a staff user opening the batch reservation modal, I want to see the 20 available dates arranged in 4 weekly rows with day-of-week labels so that I can quickly understand which dates belong together and make selections without having to cross-reference a calendar.

**Why this priority**: This is the core UX improvement — the primary pain point is the flat, unlabeled date list. Weekly grouping with day headers solves this directly.

**Independent Test**: Can be fully tested by opening the batch reservation modal and confirming that dates appear in 4 rows of 5 columns with day-of-week labels above each column (Lun, Mar, Mié, Jue, Vie).

**Acceptance Scenarios**:

1. **Given** the batch modal displays 20 available dates, **When** the modal opens, **Then** dates are arranged in exactly 4 rows with 5 dates per row.
2. **Given** the grid layout is rendered, **When** I view each row, **Then** the dates are aligned in columns under day-of-week labels (Lun through Vie).
3. **Given** two consecutive weeks are displayed, **When** I scan the grid, **Then** there is clear visual separation between week groups.
4. **Given** the grid contains dates from different months, **When** I view the labels, **Then** each date shows its day and month (e.g., 15/1, 1/2).

---

### User Story 2 - Select Dates from Weekly Grid (Priority: P2)

As a staff user selecting dates in the batch modal, I want to click date buttons to toggle selections and see real-time feedback so that I can confidently choose multiple dates and verify my selections before submitting.

**Why this priority**: Date selection is the primary interaction after viewing. The grid layout must not break existing selection behavior.

**Independent Test**: Can be tested by clicking multiple date buttons, verifying the active state toggles, and confirming the selection count updates in real-time.

**Acceptance Scenarios**:

1. **Given** the modal with the weekly grid is displayed, **When** I click a date button, **Then** the button shows an active/selected state (colored background).
2. **Given** a date is already selected, **When** I click it again, **Then** the button returns to the unselected state.
3. **Given** I have selected multiple dates, **When** I view the selection summary, **Then** the count reflects the correct number of selected dates.
4. **Given** no dates are selected, **When** I check the confirm button, **Then** it is disabled.

---

### User Story 3 - Use Modal on Smaller Screens (Priority: P3)

As a staff user accessing the batch reservation modal on a tablet or mobile device, I want the weekly grid to remain usable so that I can still select dates on smaller viewports.

**Why this priority**: Mobile usage of the admin modal is less frequent but must not regress.

**Independent Test**: Can be tested by resizing the browser to tablet (768px) and mobile (375px) widths and verifying the grid adjusts without horizontal overflow.

**Acceptance Scenarios**:

1. **Given** the modal is viewed on a tablet-width viewport (768px–1024px), **When** the grid renders, **Then** the 5-column layout is preserved but may require vertical scrolling.
2. **Given** the modal is viewed on a mobile-width viewport (< 768px), **When** the grid renders, **Then** the dates remain clickable with no horizontal overflow.

---

### Edge Cases

- What happens if fewer than 20 dates are available (e.g., a week with holidays)? Partial weeks should render with empty cells or fewer columns.
- What happens if dates are not in consecutive Monday-Friday order? The system should sort chronologically before grouping.
- What happens when many dates are selected (e.g., 15 of 20)? The selection summary should handle the full range without overflow.
- What happens when the modal is opened and closed repeatedly? The grid should render consistently each time.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The batch reservation modal MUST display available dates in a grid with 5 columns (Lun–Vie) and as many rows as needed to cover all dates.
- **FR-002**: Day-of-week labels (Lun, Mar, Mié, Jue, Vie) MUST appear above each column and repeat for each weekly row.
- **FR-003**: The grid MUST include clear visual separation between week groups (e.g., border, spacing, or background tint).
- **FR-004**: Date selection and deselection via click MUST work identically to the current implementation — only the visual layout changes.
- **FR-005**: The selection count and summary display MUST update in real-time as dates are selected or deselected.
- **FR-006**: The confirm/submit button MUST remain disabled until at least one date is selected.
- **FR-007**: The grid MUST be responsive: full 5-column layout on desktop, scrollable on tablet, no horizontal overflow on mobile.
- **FR-008**: All user-visible labels and text MUST be internationalized via i18n — no hardcoded strings.

### Key Entities

- **Available Date**: A single date on which a class slot is available for reservation. Each date belongs to a day of the week (Monday through Friday) and is displayed as a clickable button in the grid.
- **Week Group**: A set of up to 5 consecutive dates (Monday–Friday) displayed as a single row or visual group in the grid.
- **Batch Reservation Modal**: The modal dialog that displays available dates and allows users to select multiple dates for batch reservation creation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 20 dates display in exactly 4 rows of 5 columns (or N rows of 5 columns for N weeks) with day-of-week labels.
- **SC-002**: A user can visually identify which dates belong to the same week within 2 seconds of opening the modal.
- **SC-003**: Date selection behaves identically to the current implementation — click toggles selection, multiple selections allowed, confirm button disabled when empty.
- **SC-004**: The modal content fits within a standard viewport height (600–700px available) without requiring the modal itself to scroll excessively.
- **SC-005**: No horizontal scrolling is required on any device width ≥ 375px.

## Assumptions

- The batch reservation modal receives 20 dates that represent 4 weeks of Monday–Friday class slots.
- Dates are already in chronological order or close to it; any sorting needed is minimal.
- The existing modal structure (header, body with form, footer with buttons) remains unchanged — only the date display area within the body is modified.
- The hidden checkbox pattern for form submission is preserved.
- Day-of-week labels use Spanish abbreviations (Lun, Mar, Mié, Jue, Vie) to match the existing Spanish i18n of the application.
- Backend view logic for date availability and reservation creation is unchanged.
