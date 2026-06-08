# Feature Specification: Cardio Equipment Reservation

**Feature Branch**: `001-equipment-reservation`

**Created**: 2026-06-07

**Status**: Draft

**Input**: User description: "Build an application that can help me reserve equipment for cardio classes. There are classes from Monday to Friday. There are 2 classes per day: 17:30 and 18:30. The reservations will be made by a system operator or a system administrator. The equipment flagged as out of service, can't be reserved. The clients must be authenticated by email or mobile number."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operator Creates Reservation (Priority: P1)

A system operator looks up a client by email or mobile number, selects a class day and time, picks available equipment, and creates a reservation.

**Why this priority**: Creating reservations is the core business function — without it the system delivers no value.

**Independent Test**: Can be fully tested by an operator logging in, searching a client, selecting a class, choosing in-service equipment, and confirming the reservation appears in the system.

**Acceptance Scenarios**:

1. **Given** a client is registered with email "client@example.com", **When** the operator searches by that email and selects Monday 17:30 class, **Then** the system shows available equipment and allows reservation creation
2. **Given** a piece of equipment is reserved for Monday 17:30, **When** the operator tries to reserve the same equipment for the same class, **Then** the system rejects with "equipment already reserved"
3. **Given** equipment is marked "out of service", **When** the operator views equipment for a class, **Then** that equipment is not listed as available

---

### User Story 2 - Administrator Manages Equipment (Priority: P2)

A system administrator adds new cardio equipment, updates its status (in service / out of service), and views the equipment inventory.

**Why this priority**: Equipment must be manageable before the reservation system can be useful — operators need accurate availability.

**Independent Test**: Can be tested by an admin adding a new treadmill, marking an existing bike as out of service, and verifying the changes reflect in the operator's reservation view.

**Acceptance Scenarios**:

1. **Given** an admin is logged in, **When** they add a new piece of equipment with name and type, **Then** it appears as available in the operator reservation view
2. **Given** equipment exists and is currently "in service", **When** the admin marks it "out of service", **Then** operators can no longer reserve it for any class
3. **Given** equipment is "out of service", **When** the admin marks it back "in service", **Then** it becomes available for reservations again

---

### User Story 3 - Administrator Manages Class Schedule (Priority: P3)

A system administrator views and manages the weekly class schedule comprising Monday to Friday with 17:30 and 18:30 time slots.

**Why this priority**: The schedule defines the reservation grid; without accurate schedule data operators cannot place reservations.

**Independent Test**: Can be tested by an admin viewing the schedule, adding a special class time, and confirming it appears for operator reservation.

**Acceptance Scenarios**:

1. **Given** the system has the default schedule (Mon-Fri, 17:30/18:30), **When** an admin views the class calendar, **Then** all 10 weekly slots are displayed
2. **Given** a class slot has no available equipment, **When** an operator attempts to reserve, **Then** the system clearly indicates no availability

---

### Edge Cases

- What happens when all equipment for a class is out of service?
- How does the system handle a client search that matches multiple records?
- What happens if an operator tries to reserve for a past class date?
- How are overlapping reservations at 17:30 and 18:30 handled for the same client?
- What happens when equipment is marked out of service but has future reservations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate and identify clients by email address or mobile phone number
- **FR-002**: System MUST allow operators to search for clients by email or mobile number
- **FR-003**: System MUST display only in-service equipment as available for reservation
- **FR-004**: System MUST prevent reservation of equipment marked "out of service"
- **FR-005**: System MUST prevent double-booking the same equipment for the same class slot
- **FR-006**: System MUST allow operators to create reservations linking a client, equipment, and class
- **FR-007**: System MUST allow administrators to add new equipment items with name and type
- **FR-008**: System MUST allow administrators to update equipment status (in service / out of service)
- **FR-009**: System MUST allow administrators to view the class schedule
- **FR-010**: System MUST enforce reservations only within the defined schedule (Mon-Fri, 17:30 and 18:30)
- **FR-011**: System MUST restrict reservation management to operators and administrators
- **FR-012**: System MUST allow one piece of equipment per client per class slot

### Key Entities *(include if feature involves data)*

- **Client**: Person attending cardio classes, identified by email and/or mobile number
- **Equipment**: Cardio machine (e.g., treadmill, stationary bike, rowing machine) with status (in-service / out-of-service)
- **Class**: Scheduled session on a specific weekday with a specific time (17:30 or 18:30)
- **Reservation**: Booking linking one client to one equipment item for one class slot
- **User**: Staff account with role (operator or administrator) managing the system

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator can complete a reservation in under 2 minutes from login to confirmation
- **SC-002**: Out-of-service equipment never appears as reservable in the operator interface
- **SC-003**: The system prevents double-booking of any equipment for the same class slot with 100% accuracy
- **SC-004**: An administrator can update equipment status and the change reflects immediately in reservation views

## Assumptions

- Each piece of equipment serves one client per class slot (no shared equipment)
- Clients do not self-service reserve — only operators and administrators create reservations
- Equipment types are standard cardio machines (treadmills, bikes, ellipticals, rowers)
- The class schedule is stable and changes infrequently
- Operator and administrator accounts are pre-provisioned (account creation is out of scope)
- Email and mobile number are unique identifiers per client
- The system runs during business hours; no real-time notifications to clients are required
