# Data Model: Create Reservations List per Class Slot

## Entity: Reservation (existing — no new entities)

No new entities. Adds a view-layer feature on the existing `Reservation` model.

### Existing Reservation fields (relevant to this feature)

| Field | Type | Purpose |
|-------|------|---------|
| `client` | FK → `Client` | The client who reserved |
| `equipment` | FK → `Equipment` (PROTECT) | The equipment reserved |
| `class_slot` | FK → `ClassSlot` (PROTECT) | The class slot for the reservation |
| `date` | `DateField` | The date of the reservation |

### Existing constraints

```python
unique_together = ["equipment", "class_slot", "date"]
```

This enforces that each piece of equipment can be reserved at most once per class slot per date. It does NOT enforce the 1:1 client-to-equipment mapping per slot.

### Changes for this feature

**No schema changes.** The existing `unique_together` constraint already prevents the same equipment being double-booked for the same slot/date, which aligns with the clarified model.

The spec clarification states "one Client can reserve only one piece of Equipment per class slot." To fully enforce this, a second unique constraint or validation would be needed:

```python
# Future constraint (not added in this feature):
# unique_together = [("equipment", "class_slot", "date"), ("client", "class_slot", "date")]
```

For this feature, the consistency is ensured at the application layer (form/validation) since the existing reservation creation flow already uses Django forms.

**No status field added.** All existing reservations are implicitly active. The "only active/confirmed" filter from the spec is a no-op in v1 — every reservation is active because there is no cancellation flow yet. A `status` field can be added when cancellation support is introduced.

### Existing ordering (unchanged)

```python
ordering = ["-date", "class_slot__time"]
```

The reservations list query will order by `equipment__name` for display purposes (FR-004).

### Queries for this feature

The list view queries reservations filtered by `class_slot` and `date`, ordered by `equipment__name`:

```python
Reservation.objects.filter(
    class_slot=class_slot,
    date=date,
).select_related("client", "equipment", "class_slot").order_by("equipment__name")
```
