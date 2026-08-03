# Research: ForeignKey(unique=True) → OneToOneField

## Research Questions

### R1: What migration does Django generate for this change?

**Decision**: Django's `makemigrations` detects the field type change and generates an `AlterField` migration. At the database level, `ForeignKey(unique=True)` and `OneToOneField` create identical schema (a column with a foreign key constraint and a unique constraint), so the migration is a schema no-op — no data migration is needed.

**Rationale**: Both field types produce the same SQL DDL: a column with a FK constraint plus a UNIQUE constraint. The `AlterField` migration may produce no SQL at all on PostgreSQL when the underlying schema is already correct.

**Alternatives considered**:
- `SeparateDatabaseAndState` with `migrations.RunSQL` — unnecessary; the auto-generated `AlterField` is sufficient and safer.
- Manual SQL migration — overkill for this change; Django handles it automatically.

### R2: Does `Reservation.objects.filter(payment_links=None)` still work?

**Decision**: Yes. Django's ORM supports `filter(related_name=None)` on both reverse `ForeignKey` relations (returns `RelatedManager`) and reverse `OneToOneField` relations (returns `OneToOneRel` descriptor). The queryset filter syntax and SQL output are identical.

**Rationale**: Verified in codebase — the only two usages of `payment_links` (`views.py:150` and `views.py:238`) use `Reservation.objects.filter(payment_links=None)`, which is fully compatible with `OneToOneField` reverse relations.

**Alternatives considered**:
- Adding `__isnull=True` instead of `=None` — not needed; both work identically.
- Adding `hasattr` checks for instance-level access — not needed; no instance-level access exists.

### R3: Do existing indexes need manual handling?

**Decision**: No. The `Meta.indexes` list contains `models.Index(fields=["reservation"])` alongside the `unique=True` attribute. When changing to `OneToOneField`, Django preserves the implicit unique index. The explicit `Index` on `reservation` is redundant but harmless; it can be kept or removed in the migration.

**Rationale**: PostgreSQL already has both a unique constraint index and a regular index on the `reservation_id` column. The `AlterField` migration will not drop the regular index (it's defined in `Meta.indexes`, not on the field), so no action needed.

**Alternatives considered**:
- Removing the explicit `Index` — could reduce index redundancy, but not required for this fix. Deferred to future optimization.

### R4: Does `on_delete=models.CASCADE` work the same?

**Decision**: Yes. `OneToOneField` supports `on_delete=models.CASCADE` identically to `ForeignKey`. When the referenced `Reservation` is deleted, the `PaymentReservation` record is cascade-deleted.

**Rationale**: `OneToOneField` inherits from `ForeignKey` and supports all the same `on_delete` options.

### R5: Does the `related_name` semantic change?

**Decision**: The `related_name="payment_links"` attribute is preserved. When accessing via instance (`reservation.payment_links`), the return type changes from `RelatedManager` (queryset-like) to a single object (or raises `RelatedObjectDoesNotExist`). However, no code in the project accesses `payment_links` as an instance attribute — it's only used in queryset filters, which behave identically.

**Rationale**: Codebase audit confirmed zero instance-level accesses of `.payment_links`.

## Summary

The change from `ForeignKey(unique=True)` to `OneToOneField` on `PaymentReservation.reservation` is a purely cosmetic field-type substitution with no behavioral, schema, or data impact. All existing code is compatible.
