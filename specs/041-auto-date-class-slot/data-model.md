# Data Model: Auto-set Date on Class Slot Selection

## Status: No changes to data layer

This feature adds client-side calculation logic only. No new models, fields, or database migrations required.

### Existing Entities (unchanged)

| Entity | Key Fields | Role |
|--------|-----------|------|
| `ClassSlot` | `day_of_week` (0-4), `time` (TimeField), `is_active` | Source of day-of-week and time for auto-date calculation |
| `Reservation` | `class_slot` (FK), `date` (DateField) | Target — date is auto-set based on selected class_slot |

### Calculation Logic (application layer only)

- **Input**: Selected `ClassSlot.day_of_week`, `ClassSlot.time`, current server time
- **Constants**: Earliest class time per day-of-week (minimum `time` among active ClassSlots on that day)
- **Output**: ISO date string (YYYY-MM-DD) set on the `date` field
- **Storage**: None — calculated on-the-fly, persisted via form submission
