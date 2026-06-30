# Data Model: Duplicated Reservation Alert

No new entities are required. The existing `Reservation` model already captures all necessary data. This feature adds a validation layer on top of the existing model.

## Existing Entities

### Reservation

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField (PK) | Primary key |
| `status` | CharField(20) | One of: `reserved`, `used`, `unused` |
| `client` | ForeignKey → Client | The client reserving |
| `equipment` | ForeignKey → Equipment | The equipment being reserved |
| `class_slot` | ForeignKey → ClassSlot | The time slot |
| `date` | DateField | The reservation date |
| `created_by` | ForeignKey → User | Operator who created it |
| `updated_by` | ForeignKey → User | Operator who last updated it |
| `notes` | TextField | Optional notes |
| `created_at` | DateTimeField (auto) | Creation timestamp |
| `updated_at` | DateTimeField (auto) | Last update timestamp |

**Uniqueness constraint**: `unique_together = ["equipment", "class_slot", "date"]`

**Duplicate detection query**:
```
Reservation.objects.filter(
    equipment=<selected_equipment>,
    class_slot=<selected_slot>,
    date=<selected_date>,
    status="reserved",
).exclude(pk=<current_pk_if_editing>).exists()
```

### Equipment

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField (PK) | Primary key |
| `name` | CharField(100) | Equipment name |
| `status` | CharField(20) | `in-service` or `out-of-service` |

Only equipment with `status="in-service"` is shown in the reservation form.

### ClassSlot

Expected fields include `time` and `is_active`. Used to filter active slots.

## Validation Rules (from FR-001, FR-004, FR-008)

1. A reservation is considered a duplicate when a `Reservation` record exists with the same `equipment`, `class_slot`, and `date`, AND that record has `status="reserved"`.
2. Reservations with status `used` or `unused` are NOT considered duplicates.
3. The duplicate check runs both on equipment selection (client-side) and on form submission (server-side).
4. On form submission, the check reads from the database (not stale/cached data) per FR-010.

## State Transitions

This feature does not introduce new state transitions. The existing `Reservation` status lifecycle remains unchanged:

```
reserved → used
reserved → unused
```

The alert only triggers when the target reservation status is `reserved` — it does not affect transitions.
