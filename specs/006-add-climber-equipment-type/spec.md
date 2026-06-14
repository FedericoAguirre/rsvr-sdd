# Feature Specification: Add Climber Equipment Type

**Feature Branch**: `007-add-climber-equipment-type`

**Created**: 2026-06-13

**Status**: Draft

**Input**: User description: "As an Operator and Administrator I want to add the Climber (Escaladora) option in EQUIPMENT_TYPES options, for correctly naming the equipment type. This type must be the defaulted option and the first one to select."

## User Scenarios & Testing

### User Story 1 - Select Climber as equipment type when creating equipment (Priority: P1)

An Operator or Administrator creating or editing an equipment record sees "Climber (Escaladora)" as the first and default option in the equipment type dropdown, ensuring gym equipment is correctly categorized.

**Why this priority**: Core feature — without the Climber type being available and default, the feature has no value.

**Independent Test**: Can be tested by navigating to the equipment creation form and verifying the Climber option is present and pre-selected.

**Acceptance Scenarios**:

1. **Given** the Operator is on the equipment creation form, **When** they view the equipment type dropdown, **Then** "Climber (Escaladora)" appears as the first option in the list
2. **Given** the Operator opens the equipment creation form, **When** no previous type is selected, **Then** the Climber option is pre-selected by default
3. **Given** an existing equipment record of any type is being edited, **When** the form loads, **Then** its current type is selected (not overridden to Climber)

---

### User Story 2 - Pre-seeded Climber equipment exists in the system (Priority: P1)

The system comes with 30 Climber equipment records pre-seeded, named sequentially E01 through E30, so Operators and Administrators can immediately reference and manage them without manual creation.

**Why this priority**: The seed data is required for the feature to be useful — without it the Climber type exists but there are no associated equipment to work with.

**Independent Test**: Can be tested by checking that Equipment records with names E01 through E30 of type Climber exist after a fresh setup.

**Acceptance Scenarios**:

1. **Given** the system has been freshly set up with migrations, **When** the Operator views the equipment list, **Then** 30 Climber equipment records named E01 through E30 are visible
2. **Given** the 30 seeded Climber equipment exist, **When** the Operator views any of them, **Then** each has the correct Climber type assigned

### Edge Cases

- What happens when an Administrator changes the default equipment type in future releases? The change only affects new forms; existing unset records retain their stored value.
- What happens if additional Climber equipment is manually added with names outside the E01-E30 range? They coexist without conflict since the seed migration only inserts if the migration hasn't been applied yet.
- What happens when the seed migration is rolled back? All Climber equipment with names starting with "E" are removed.

## Requirements

### Functional Requirements

- **FR-001**: The EQUIPMENT_TYPES list MUST include a "Climber" (db value: "climber") option as the first entry
- **FR-002**: The Climber option MUST be the default selection when creating new equipment
- **FR-003**: The system MUST be delivered with 30 Climber equipment records named E01 through E30 created via data migration
- **FR-004**: All existing equipment types (Treadmill, Stationary Bike, Elliptical, Rowing Machine, Other) MUST continue to function unchanged
- **FR-005**: All existing equipment records MUST preserve their type when the Climber type is added (no data migration affects existing records)

### Key Entities

- **Equipment**: Represents a piece of gym equipment. Key attributes: name (string), equipment_type (choice from EQUIPMENT_TYPES), status, notes. The Equipment model's EQUIPMENT_TYPES choice list is extended with the "climber" option.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator or Administrator can create a new equipment record with Climber as the type in under 2 clicks from the equipment creation form
- **SC-002**: 30 Climber equipment records (E01-E30) exist in the system immediately after running database migrations
- **SC-003**: All existing equipment records and types remain accessible and unchanged after the migration is applied
- **SC-004**: The Climber option appears first in the equipment type dropdown, above all pre-existing types

## Assumptions

- The existing Equipment model, form, templates, and admin interface dynamically render EQUIPMENT_TYPES choices — no template changes are needed when adding a new type
- The operator and administrator roles already have permission to create and edit equipment
- Seed data is idempotent (the migration checks if it has been applied, not if data already exists)
- Equipment names E01-E30 follow a "C" prefix pattern (existing seed data in dev may use different naming; the migration inserts fresh records)
