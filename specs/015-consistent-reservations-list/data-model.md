# Data Model: Consistent Reservations List

No new entities are introduced by this feature. The existing `Reservation` model already provides all fields needed for the unified table display.

## Reservation

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `date` | DateField | Direct attribute | Displayed in "Date" column |
| `client` | ForeignKey → Client | `r.client` | "Client" column uses `r.client|full_name` |
| `class_slot` | ForeignKey → ClassSlot | `r.class_slot` | "Class" column |
| `equipment` | ForeignKey → Equipment | `r.equipment` | "Equipment" column |
| `status` | CharField (choices) | `r.get_status_display` | "Status" column (translated) |
| `pk` | AutoField | `r.pk` | "View" button URL parameter |

## Entity Relationships

```
Reservation ──belongs to──→ Client
Reservation ──has──→ Equipment
Reservation ──has──→ ClassSlot
Reservation ──created by──→ User
```

## Scope of Change

The fix is isolated to template rendering — the data model, querysets, and views remain unchanged. The `reservation_list` view already passes all necessary related objects via `select_related("client", "equipment", "class_slot")`.
