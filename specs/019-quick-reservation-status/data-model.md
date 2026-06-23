# Data Model: Quick Reservation Status Management

## Entity: Reservation

The `Reservation` model already exists. This feature **adds no new entities or fields** — it only adds new interaction patterns on top of the existing `status` field.

### Fields (existing — relevant subset)

| Field | Type | Purpose |
|-------|------|---------|
| `status` | CharField (max 20) | Current status: `"reserved"`, `"used"`, or `"unused"`. Default: `"reserved"`. |
| `client` | ForeignKey → Client | Climber who made the reservation |
| `equipment` | ForeignKey → Equipment | Equipment reserved |
| `class_slot` | ForeignKey → ClassSlot | Class time slot |
| `date` | DateField | Date of the reservation |
| `created_by` | ForeignKey → User | Who created the reservation |
| `updated_by` | ForeignKey → User | Who last updated the reservation (auto-set on status change) |

### Status State Transitions

```text
                  ┌──────────┐
                  │ reserved │
                  └────┬─────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
          ┌──────┐ ┌──────┐ ┌────────┐
          │ used │ │unused│ │reserved│
          └──┬───┘ └──┬───┘ └────────┘
             │        │
             │        │
             ▼        ▼
          ┌──────┐ ┌──────┐
          │unused│ │ used │
          └──────┘ └──────┘
```

- A reservation can transition between any of the three states freely.
- No validation restricts transitions based on time (past/future dates) or capacity.
- The `updated_by` field is set to the current user when a status change occurs.

### Validation Rules

| Rule | Enforcement |
|------|-------------|
| Status must be one of: `reserved`, `used`, `unused` | Django `choices` constraint + view-level validation |
| Only one reservation per equipment + class_slot + date | Database `unique_together` constraint (existing) |

### Notes

- No database migrations required for this feature.
- The `updated_by` field is currently set by the view on save; this behavior continues.
