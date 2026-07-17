# Feature Specification: Switch Date and Class Block Columns in Payments, Add Stripe

**Feature Branch**: `044-payments-columns-stripe`

**Created**: 2026-07-16

**Status**: Draft

**Input**: User description: "Switch date and class block columns in payments reservations grid, add stripe for better visualization"

## User Scenarios & Testing

### User Story 1 - Reorder and Stripe the Reservations Grid on Payment Detail Page (Priority: P1)

As an app operator viewing the "Reservas asociadas" section on the `payments/{id}/` page, I want the columns to appear as Bloque de clase, Fecha, Equipo, Estado so that I can identify the class block and date more easily at a glance. I also want the grid rows to alternate in background color (striped) for improved readability across multiple entries.

**Why this priority**: This is the only user story for this feature. The grid reorder and striping are a single, atomic visual change to one page.

**Independent Test**: Open any payment detail page that has associated reservations and verify the column headers appear in order: Bloque de clase, Fecha, Equipo, Estado, and that table rows have alternating background colors.

**Acceptance Scenarios**:

1. **Given** I am viewing the "Reservas asociadas" section on the `payments/{id}/` page, **When** the reservation list loads, **Then** the columns appear in the order: Bloque de clase, Fecha, Equipo, Estado.
2. **Given** I navigate between different payment detail pages, **When** each page loads, **Then** the column order remains Bloque de clase, Fecha, Equipo, Estado consistently.
3. **Given** I am viewing the reservation grid on a payment detail page, **When** the table renders, **Then** rows have alternating background colors (striped) for readability.
4. **Given** a payment has no associated reservations, **When** the page loads, **Then** the "Reservas asociadas" section is not displayed (no empty table).

### Edge Cases

- Payment with zero reservations: the reservations section should be hidden entirely (no empty table rendered)
- Payment with a single reservation: the single row should appear with correct column order and striping (single row still renders with stripe class)
- Page refresh or direct navigation: the column order and striping persist across all navigation methods

## Requirements

### Functional Requirements

- **FR-001**: The "Reservas asociadas" table on the payment detail page MUST display columns in the order: Bloque de clase, Fecha, Equipo, Estado.
- **FR-002**: The "Reservas asociadas" table MUST have alternating row background colors (striped).
- **FR-003**: The column order MUST be consistent across all navigation methods (direct URL, page refresh, browser back/forward).
- **FR-004**: The striping MUST apply regardless of the number of rows (including a single row).
- **FR-005**: When a payment has no associated reservations, the "Reservas asociadas" section MUST NOT be displayed.

### Key Entities

- **Payment**: The financial record whose detail page contains the reservations grid. A payment can have zero or more associated reservation payments.
- **ReservationPayment**: The join entity linking a reservation to a payment. Each entry in the grid represents a reservation associated with the payment.
- **Reservation**: A booking for a specific class slot and date. Contains the class slot, date, equipment, and status displayed in the grid.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The column headers on any payment detail page with reservations are visibly ordered as: Bloque de clase, Fecha, Equipo, Estado.
- **SC-002**: Table rows display with alternating background colors identifiable by visual inspection.
- **SC-003**: The column order and striping remain consistent across page reloads and navigation between payment detail pages.
- **SC-004**: No existing functionality (links, status badges, payment data) is altered or removed.

## Assumptions

- The application already uses Bootstrap 5, which provides the `table-striped` CSS class for alternating row colors.
- The current column translate-able labels (Date, Equipment, Class Slot, Status) are already defined in the project's locale files.
- Only the `payments/{id}/` template needs to change; no backend logic, model, or view modifications are required.
- The previous feature (043) changed a similar grid on `clients/{id}/` — this feature applies the same pattern to `payments/{id}/`.
