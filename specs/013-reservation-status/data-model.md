# Data Model: Reservation Status

## Entity: Reservation (Modified)

### New Field

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `status` | `CharField` | `max_length=20`, `choices=STATUS_CHOICES` | `"reserved"` | Current attendance status of the reservation |

### Status Choices

| DB Value | Display Label (en) | Display Label (es) | Description |
|----------|-------------------|-------------------|-------------|
| `reserved` | Reserved | Reservado | Client has a reservation for the slot (initial/default state) |
| `used` | Used | Usado | Client attended the class |
| `unused` | Unused | No usado | Client did not attend the class |

### State Transitions

```
  ┌──────────┐
  │ reserved │◄────────────────────┐
  └────┬─────┘                      │
       │                            │
    ┌──┴──┐                         │
    │     │                         │
    ▼     ▼                         │
 ┌──────┐ ┌────────┐               │
 │ used │ │ unused │               │
 └──────┘ └────────┘               │
    │         │                    │
    └────┬────┘                    │
         │                         │
         └──────► (back to reserved)
```

All transitions are bidirectional. Any status can be changed to any other status by an authorized user (Administrator or Operator).

### Validation Rules

- `status` field is required (always has a value)
- Only Administrators and Operators (staff users) can change reservation status
- No automatic status transitions (all changes are manual)

### Migration Impact

- New migration `0003_reservation_status` adds the `status` field to existing `Reservation` table
- Existing reservations automatically get `status = "reserved"` (the default)
- No data migration needed; default value handles backward compatibility

### Model Code Pattern (Reference)

Follows the existing pattern from `Equipment.status`:

```python
STATUS_CHOICES = [
    ("reserved", _("Reserved")),
    ("used", _("Used")),
    ("unused", _("Unused")),
]
status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="reserved",
    verbose_name=_("status"),
)
```
