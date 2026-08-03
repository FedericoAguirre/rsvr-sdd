# Data Model: Remove ClassPrice-ClassSlot Association

**Date**: 2026-08-02
**Spec**: `specs/059-remove-classslot-association/spec.md`
**Contract**: `contracts/README.md`

## Purpose

Define the data entities after the `class_slot` ForeignKey removal from `ClassPrice`, their fields, validation rules, state transitions, and relationships.

## Entities

### ClassSlot (existing — unchanged)

The project's "class" entity (Spanish: "Bloque de clase"). **Not modified** by this feature. No longer referenced by `ClassPrice`.

### ClassPrice (MODIFIED — class_slot removed)

A versioned, standalone price record. The `class_slot` ForeignKey is **removed**.

| Field | Type | Rule |
|-------|------|------|
| `id` | Auto PK | surrogate key |
| `price` | Decimal(10, 2) | the price amount; **immutable once created** |
| `current` | Boolean | default True; `True` = active price (no per-class constraint; multiple current prices may exist globally) |
| `created_by` | FK → User | who entered this price; **required**; PROTECT on delete |
| `created_at` | DateTime | auto_now_add; the effective date |
| `changed_at` | DateTime | nullable; when this price was retired/superseded |
| `changed_by` | FK → User (nullable) | who retired this price; PROTECT on delete |
| `updated_at` | DateTime | auto_now; last touch |

**`class_slot` field**: **REMOVED**. Migration `0004_remove_classprice_class_slot.py` drops the column.

**Filtered UniqueConstraint `unique_current_classprice_per_slot`**: **REMOVED**. No longer needed since there is no per-class current-price grouping.

### User (existing — Django auth, referenced)

The administrator who creates or retires a price. Referenced via `created_by` and `changed_by`.

## Validation Rules

| Rule | Mechanism | Source |
|------|-----------|--------|
| Price immutable once created | `save()` calls `full_clean()` → `clean()` raises `IntegrityError` if price differs from DB value | Spec AC |
| Records never deleted | `delete()` overridden to raise `PermissionDenied`; `ClassPriceManager.delete()` + `ClassPriceQuerySet.delete()` overridden; admin `has_delete_permission=False`; user FKs use `PROTECT` | Research Decision 3 |
| Atomicity of price creation | `@transaction.atomic` in `enter_price()` | Research Decision 2 |
| Administrator-only changes | `UserPassesTestMixin` test_func: `is_superuser` or in `Administrators` group | Spec FR-011 |
| Attribution always captured | `created_by` required; `changed_by` set on retire | Spec AC |

## State Transitions

- **`ClassPrice.current`**:
  - `True` (created) — when a price is first entered (standalone, no class association).
  - The retire-and-create swap (previous `True → False`) is **removed** — without a class grouping, `enter_price` simply creates a new record with `current=True`. The `current` flag and `changed_at`/`changed_by` fields are retained for historical/retire use if/when a class association is added later.

## Relationships (summary)

```text
User 1──* ClassPrice  (as created_by)
User 1──* ClassPrice  (as changed_by, only on retired records)
```

The `ClassSlot 1 — * ClassPrice` relationship is **removed**. `ClassPrice` is now a standalone entity with no foreign data-model relationship to `ClassSlot`.
