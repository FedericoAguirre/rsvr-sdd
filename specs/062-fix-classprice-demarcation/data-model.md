# Data Model: Fix ClassPrice Demarcation

**Feature**: 062-fix-classprice-demarcation
**Date**: 2026-08-02

## Entities

### ClassPrice (No Schema Changes)

No new fields, no migrations. All fields below already exist.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| `id` | `BigAutoField` (PK) | NOT NULL | Implicit |
| `price` | `DecimalField(10,2)` | NOT NULL | Immutable after creation |
| `current` | `BooleanField` | NOT NULL, default `True` | `True` → active price; `False` → archived |
| `created_by` | `FK → User` | NOT NULL, PROTECT | Who created the record |
| `created_at` | `DateTimeField` | NOT NULL, auto_now_add | When the record was created |
| `changed_at` | `DateTimeField` | NULLABLE | Set when this price is superseded (was never populated before this fix) |
| `changed_by` | `FK → User` | NULLABLE | Who superseded this price (was never populated before this fix) |
| `updated_at` | `DateTimeField` | NOT NULL, auto_now | Last modified timestamp |

### State Transition

The `current` field undergoes a one-way transition:

```
current=True ──[new price entered]──> current=False
                                      changed_at = timezone.now()
                                      changed_by = <admin user>
```

- Once a price is archived (`current=False`), it can never become current again through normal app flow.
- The `current=True` → `current=False` transition is irreversible via the app (prices cannot be reactivated).

### Invariants

1. **At most one current price** is expected after any `enter_price()` call (not enforced by constraint, but enforced by the update logic).
2. **Price immutability**: Once created, `price` cannot be modified (`clean()` enforces this).
3. **No deletion**: Prices are never deleted — only archived.
4. **Audit trail**: Every archived price records who superseded it (`changed_by`) and when (`changed_at`).

### Relationships

```
ClassPrice.created_by ──FK(PROTECT)──> User
ClassPrice.changed_by ──FK(PROTECT)──> User (nullable)
```

No relationship to `ClassSlot` (decoupled in migration 0004).
