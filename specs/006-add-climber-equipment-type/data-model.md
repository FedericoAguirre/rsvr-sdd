# Data Model: Add Climber Equipment Type

## Entity: Equipment

No new entities. Existing `Equipment` model's `EQUIPMENT_TYPES` choice list is extended.

### EQUIPMENT_TYPES (after change)

| Db value | Display label |
|----------|--------------|
| `climber` | Climber (Escaladora) |
| `treadmill` | Treadmill |
| `bike` | Stationary Bike |
| `elliptical` | Elliptical |
| `rower` | Rowing Machine |
| `other` | Other |

The `equipment_type` field is a `CharField(max_length=50, choices=EQUIPMENT_TYPES)`. No schema migration needed — choices are not reflected in the database schema.

### Seed Data

| Field | Value |
|-------|-------|
| `name` | E01 through E30 |
| `equipment_type` | `"climber"` |
| `status` | `"in-service"` (default) |
| `notes` | `""` (blank) |

Created as 30 Equipment objects via `bulk_create` in migration `0002_seed_climber_equipments.py`.

### Validation Rules

- `equipment_type` must be one of the EQUIPMENT_TYPES choices (enforced by Django model validation)
- `name` is required, max 100 chars (unchanged from existing model)
