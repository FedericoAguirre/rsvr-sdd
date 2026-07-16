# Feature Specification: Switch Date and Class Block Columns in Payments History

**Feature Branch**: `043-switch-date-class-columns`

**Created**: 2026-07-16

**Status**: Draft

**Input**: User description: "Switch data and class block columns in the payments history"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reorder Reservation History Columns (Priority: P1)

As an app operator viewing the client detail page, I want the reservation history columns to appear as Clase, Fecha, Equipo (instead of the current order), so that I can identify the class day and date at a glance without scanning across the table.

**Why this priority**: This is the only requirement — the entire feature is a single focused change to the column order in the reservation history table on the client detail page.

**Independent Test**: Load any client detail page with reservations and verify the column headers appear in the order: Clase, Fecha, Equipo.

**Acceptance Scenarios**:

1. **Given** I am viewing the "Historial de Reservas" section on a `clients/{id}/` page, **When** the reservation list loads, **Then** the columns appear in the order: Clase, Fecha, Equipo.
2. **Given** I navigate between different client detail pages, **When** each page loads, **Then** the column order remains Clase, Fecha, Equipo consistently.
3. **Given** the page is refreshed or reloaded, **When** the reservation history renders, **Then** the column order is still Clase, Fecha, Equipo.

---

### Edge Cases

- **No reservations**: Client with zero reservation history — the column headers still display in the new order (Clase, Fecha, Equipo) even though the table body is empty.
- **Single reservation**: Only one row is affected — column order change is still visible and consistent.
- **New reservation added**: After a new reservation is created, the history table still uses the new column order.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The reservation history table on `clients/{id}/` MUST display columns in the order: Clase (class block), Fecha (date), Equipo (equipment).
- **FR-002**: The column order change MUST apply consistently across all page views (initial load, client navigation, page refresh).
- **FR-003**: No existing functionality (links, sorting, filtering, data display) may be altered — only the column order changes.
- **FR-004**: The column header labels MUST remain unchanged — only their visual order is rearranged.

### Key Entities

- **Reservation**: Represents a booked class session displayed in the history table. The entity itself is unaffected — only the display order of its columns changes.
- **Payment**: Groups reservations for payment purposes. The client detail page shows reservation history associated with the client, not with a specific payment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On any `clients/{id}/` page with reservation history, the column order is always Clase, Fecha, Equipo on every page load.
- **SC-002**: The column order change introduces zero regressions — all existing interactions (sorting, filtering, navigation) continue to work identically.
- **SC-003**: The change is purely visual — no data is added, removed, or modified in the process.

## Assumptions

- The current column order is Fecha, Clase, Equipo (this is the order to be changed).
- The change is limited to the `clients/{id}/` page only — no other pages or sections are affected.
- The column headers, data content, and underlying data model remain unchanged.
- No responsive/mobile breakpoint handling changes are required — the same order applies at all screen sizes.
- The template uses standard Django template rendering with a table structure that can be reordered at the template level.
