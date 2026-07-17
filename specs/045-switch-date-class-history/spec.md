# Feature Specification: Switch date and class block columns in history

**Feature Branch**: `045-switch-date-class-history`

**Created**: 2026-07-16

**Status**: Draft

**Input**: Switch date and class block columns in the payments history on the client detail page

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reorder reservation history columns on client detail (Priority: P1)

As an app operator, I want to switch the date and class block column order in the reservation history table on the client detail page, so that I can identify the class and the date more easily at a glance.

**Why this priority**: This is the only change required for this feature — a single UI reorder on the client detail page with no dependencies.

**Independent Test**: Can be fully tested by navigating to any client detail page and verifying the "Historial de Reservas" table columns appear in the order: Clase, Fecha, Equipo.

**Acceptance Scenarios**:

1. **Given** I am viewing the "Historial de Reservas" section on the `clients/{id}/` page, **When** the reservation list loads, **Then** the columns appear in the order: Clase, Fecha, Equipo.
2. **Given** I navigate between different client detail pages, **When** each page loads, **Then** the column order remains Clase, Fecha, Equipo consistently.
3. **Given** the page is refreshed or reloaded, **When** the reservation history renders, **Then** the column order is still Clase, Fecha, Equipo (persistent across requests).

---

### Edge Cases

- What happens when a client has no reservations? The empty state message should still render correctly with no column ordering issues.
- What happens if a reservation has no class slot assigned? The class slot cell should display as empty/null without breaking the column alignment.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The reservation history table on the client detail page MUST display columns in the order: Class, Date, Equipment.
- **FR-002**: The column order MUST be consistent across all client detail pages, regardless of navigation method (direct URL, search results, payment links, etc.).
- **FR-003**: The column order MUST persist across page refreshes and reloads.
- **FR-004**: No existing functionality (links, status display, data formatting) MUST be affected by the column reorder.
- **FR-005**: The empty state message MUST still display correctly when a client has no reservation history.

### Key Entities *(include if feature involves data)*

No new entities are introduced. The existing data model (Client, Reservation, ClassSlot, Equipment) is unaffected. Only the presentation order of existing columns changes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On any `clients/{id}/` page, the three reservation history columns render in the order: Clase (first), Fecha (second), Equipo (third).
- **SC-002**: No new errors or regressions are introduced in the client detail page (existing links, formatting, and data display remain unchanged).
- **SC-003**: The empty state for clients with no reservations renders correctly with no column header rendering issues.

## Assumptions

- The existing DTL (Django Template Language) `{% translate %}` tags with translations for "Date", "Class", and "Equipment" are already in place and will be reused.
- The change is limited to the template file; no model, view, URL, or JavaScript changes are required.
- The client detail page already has an empty state message for clients with no reservations, and it will not be affected by the reorder.
- The existing `table-striped` class (already applied) will remain unchanged.
