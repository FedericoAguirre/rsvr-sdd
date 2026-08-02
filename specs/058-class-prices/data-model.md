# Data Model: Class Price Versioning & Audit

**Date**: 2026-08-02
**Spec**: `specs/058-class-prices/spec.md`
**Contract**: `contracts/README.md`

## Purpose

Define the data entities introduced or referenced by this feature, their fields, validation rules, state transitions, and relationships — grounded in the existing `ClassSlot` and `Payment` models (see Research Decision 1 & 5).

## Entities

### ClassSlot (existing — referenced)

The project's "class" entity (Spanish: "Bloque de clase"). Not modified by this feature.

| Field | Type | Rule |
|-------|------|------|
| `day_of_week` | Integer (Mon–Fri, 0–4) | choices; part of unique (day, time) |
| `time` | Time | choices 17:30/18:30; part of unique (day, time) |
| `is_active` | Boolean | default True; toggles availability |

### ClassPrice (NEW)

The versioned price record for a single class (ClassSlot). This is the new model introduced by the feature.

| Field | Type | Rule |
|-------|------|------|
| `id` | Auto PK | surrogate key |
| `class_slot` | FK → `classes.ClassSlot` | **PROTECT** on delete (never orphan history); the priced class |
| `price` | Decimal(10, 2) | the price amount; **immutable once created** |
| `current` | Boolean | default True; `True` = active price |
| `created_by` | FK → User | who entered this price; **required** |
| `created_at` | DateTime | auto_now_add; the effective date (when this version became active) |
| `changed_at` | DateTime | nullable; when this price was retired/superseded |
| `changed_by` | FK → User (nullable) | who retired this price |
| `updated_at` | DateTime | auto_now; last touch |

### User (existing — Django auth, referenced)

The administrator who creates or retires a price. Referenced via `created_by` and `changed_by`. Permissions: only members of the `Administrators` group (or superuser) may enter prices — per the existing `UserPassesTestMixin` guard pattern.

## Validation Rules

| Rule | Mechanism | Source |
|------|-----------|--------|
| Only one current price per class | Filtered `UniqueConstraint(fields=["class_slot"], condition=Q(current=True))` | Research Decision 2; Django docs |
| Price value immutable once created | Enforced in service/view logic (write-once `price`); model does not expose price edits after creation | Spec AC: prices immutable |
| Records never deleted | `delete()` overridden to raise; admin `has_delete_permission=False`; `on_delete=PROTECT` | Research Decision 3; Django `Collector.delete` / ProtectedError |
| Every price change atomic | `@transaction.atomic` + `select_for_update(of=("self",))` around the retire-and-create swap | Research Decision 4; Django docs |
| Administrator-only changes | `UserPassesTestMixin` test_func: `is_superuser` or in `Administrators` group | `PaymentExportView`/`PaymentReportView` |
| Attribution always captured | `created_by` required; `changed_by` set on retire | Spec AC (attribution); `Payment` pattern |

## State Transitions

- **`ClassPrice.current`**:
  - `True` (created) — when a price is first entered for a slot that has no current price.
  - `True → False` — when a new price is entered for a slot that already has a current price; at this transition `changed_at` and `changed_by` are stamped.
  - Once `False`, the record is **immutable** in its price value and creation metadata; only `changed_at`, `changed_by`, and `updated_at` are written at the transition, and never afterward.
- A slot always has **at most one** `current=True` record (enforced by the filtered unique constraint).

## Relationships (summary)

```
ClassSlot 1──* ClassPrice
User 1──* ClassPrice  (as created_by)
User 1──* ClassPrice  (as changed_by, only on retired records)
```

The new relationship is `ClassSlot 1 — * ClassPrice`. No existing model is modified.
