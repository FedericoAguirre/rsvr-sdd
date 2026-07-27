# Feature Specification: List Unassociated Reservations on Payments Page

**Feature Branch**: `051-list-unassociated-reservations`

**Created**: 2026-07-24

**Status**: Draft

**Input**: Using @ai/features/todos/15-list-unassociated-user-reservations.md create the new feature specs

## User Scenarios & Testing

### User Story 1 - View Unassociated Reservations for a Client (Priority: P1)

As a staff user viewing the payments page for a specific client, I want to see only the client's reservations that are not yet associated with a payment so that I can quickly identify which reservations still need payment follow-up.

**Why this priority**: This is the only user workflow — the entire feature is showing a pre-filtered list of unassociated reservations on the payments client detail page.

**Independent Test**: Can be fully tested by navigating to the `/payments/{client_id}` page for a client who has a mix of associated and unassociated reservations, and verifying that only the unassociated ones appear in the list.

**Acceptance Scenarios**:

1. **Given** a client has reservations both associated and not associated with a payment, **When** I access `/payments/{client_id}`, **Then** only the reservations without a payment association appear in the list.
2. **Given** a client has no reservations at all, **When** I access `/payments/{client_id}`, **Then** the page shows an appropriate empty-state message (e.g., "No hay reservaciones sin asociar").
3. **Given** all of a client's reservations are already associated with a payment, **When** I access `/payments/{client_id}`, **Then** the page shows an empty-state message indicating no unassociated reservations exist.
4. **Given** I create a new reservation for the same client after the page loads, **When** I refresh the page, **Then** the new reservation appears in the list (since it has no payment association yet).

---

### Edge Cases

- What happens when the client ID is invalid or the client doesn't exist? The page should show a 404 or appropriate error message (existing behavior).
- What happens when a reservation is associated with a payment while viewing the page? The reservation should no longer appear after the page is refreshed, since it now has a payment association.
- What happens when a client has a very large number of unassociated reservations? The list should be paginated following the existing pagination pattern.
- What happens when the user navigates away from the page and returns? The list reloads fresh data, reflecting any new associations or new reservations.

## Requirements

### Functional Requirements

- **FR-001**: The `/payments/{client_id}` page MUST display only reservations belonging to the specified client that have no associated payment.
- **FR-002**: The system MUST filter reservations by matching `client_id` against the client parameter in the URL.
- **FR-003**: The system MUST exclude any reservation that is linked to a payment via the PaymentReservation relationship from the displayed list.
- **FR-004**: The system MUST display an appropriate empty-state message when no unassociated reservations exist for the client.
- **FR-005**: Newly created reservations for the client (which have no payment association) MUST appear in the filtered list on next page load.
- **FR-006**: The reservation list MUST be paginated following the existing pagination conventions used elsewhere in the payments module.
- **FR-007**: The reservation list MUST preserve the existing ordering (e.g., by date, then by class slot time).

### Key Entities

- **Client**: The person whose reservations are being viewed. Identified by `client_id` in the URL.
- **Reservation**: A class booking linked to a client. May optionally be associated with a payment via a PaymentReservation link.
- **Payment**: A payment record that can be associated with one or more reservations.
- **PaymentReservation**: The linking entity that connects a reservation to a payment. Reservations with an existing PaymentReservation link are excluded from the filtered list.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A staff user can see exactly which reservations for a client still need payment — no associated reservations appear in the list.
- **SC-002**: The filtered list loads in the same amount of time as the existing unfiltered reservations list for the same client.
- **SC-003**: Empty states are shown when appropriate (client has no reservations; all reservations are already associated).
- **SC-004**: New reservations for the client appear automatically on next page load, without manual re-filtering.

## Assumptions

- The existing PaymentReservation model (linking Payment to Reservation) already exists and is correctly maintained by the payment association workflow.
- The `/payments/{client_id}` page already exists and currently displays all reservations for that client (or has some other unfiltered behavior).
- The filtering applies only to the reservations list on the client detail payments page — other areas of the system are unaffected.
- Existing pagination and ordering behavior from the current reservations list is reused.
- The page is accessed by authenticated staff users with appropriate permissions (existing role-based access is unchanged).
