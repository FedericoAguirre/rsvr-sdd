# Data Model: Switch Date and Class Block Columns in Payments History

**Status**: No changes to data model

## Database

No database schema changes. This feature is purely a presentation-layer template reorder.

## Entities Referenced

| Entity | Usage | Change |
|--------|-------|--------|
| `Reservation.date` | Displayed as "Fecha" column | None — only column position changes |
| `Reservation.class_slot` (FK → `ClassSlot`) | Displayed as "Clase" column | None — only column position changes |
| `Reservation.equipment` (FK → `Equipment`) | Displayed as "Equipo" column | None — only column position changes |

## Validation Rules

No new validation rules.
