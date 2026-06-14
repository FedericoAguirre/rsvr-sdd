# Contracts: Add Climber Equipment Type

**No external interfaces.** This feature is purely internal:

- Equipment model change (EQUIPMENT_TYPES list) — affects Django forms and admin dynamically; no endpoint contract changes
- Data migration `0002_seed_climber_equipments.py` — internal, reversible migration

All existing API endpoints (`/equipment/`, `/equipment/create/`, etc.) continue to work unchanged.
