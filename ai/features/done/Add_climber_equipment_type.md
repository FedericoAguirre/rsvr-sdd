# Add the Climber option in EQUIPMENT_TYPES options

## Description

As an Operator and Administrator I want to add the Climber (Escaladora) option in EQUIPMENT_TYPES options, 
for correctly naming the equipment type.

This type must be the defaulted option and the first one to select.

A second goal is to have 30 equipments set to Climber and named from E01, E02, ... , E10, E11, ... , E30.
These equipments must be added as a data seed.

## Inputs

- The @backend/apps/equipment/models.py file.
- The EQUIPMENT_TYPES list
- The Equipment class

## Outputs

- The Climber option in the EQUIPMENT_TYPES list.
- All related assets modified, under the @backend/apps/equipment folder.
- All related tests modified as needed.

## Acceptance criteria

- The Climber option exists in the EQUIPMENT_TYPES list, used as default.
- The related assets modified, under the @backend/apps/equipment folder are updated accordingly.
- All related tests execute correctly.
- The list of 30 equipments exists in the application.
