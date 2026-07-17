# Data Model: Update Auto-Date Algorithm

## Entities

No new entities, fields, or relationships. This feature changes the calculation logic only.

| Entity | Status |
|--------|--------|
| `Reservation` | Unchanged — existing `date` and `class_slot` fields |
| `ClassSlot` | Unchanged — existing `day_of_week` field (0=Mon..6=Sun) |

## Validation Rules (unchanged)

- `(equipment, class_slot, date)` uniqueness enforced in `ReservationForm.clean()`
- Missing class_slot → date field unmodified
- Manual date override → no recalculation on class slot change
