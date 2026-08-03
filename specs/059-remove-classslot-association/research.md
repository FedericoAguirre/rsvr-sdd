# Research: Remove ClassPrice-ClassSlot Association

**Date**: 2026-08-02
**Spec**: `specs/059-remove-classslot-association/spec.md`
**Plan**: `specs/059-remove-classslot-association/plan.md`

## Purpose

Resolve all unknowns in the plan's Technical Context so that the refactoring is grounded in the actual codebase and current Django documentation (Constitution Principle V). The key unknowns are: how to cleanly remove a ForeignKey field + filtered UniqueConstraint in a migration, how to rework the `enter_price` service without a class context, and how to adjust views/URLs/templates.

## Method

Read-only inspection of the existing codebase (the `058-class-prices` implementation) plus authoritative Django documentation fetched via Context7 (library ID `/django/django`).

- `backend/apps/classes/models.py` — current `ClassPrice` model (class_slot FK, filtered UniqueConstraint, enter_price service, delete prevention).
- `backend/apps/classes/admin.py` — `ClassPriceAdmin` with class_slot in list_display, search_fields, readonly_fields.
- `backend/apps/classes/views.py` — `ClassPriceCreateView` (uses class_slot pk from URL) + `ClassPricesView` (filters by class_slot).
- `backend/apps/classes/urls.py` — routes `classes/<int:pk>/prices/` and `classes/<int:pk>/prices/add/`.
- `backend/apps/classes/templates/classes/class_prices.html` + `class_price_form.html` — templates referencing class_slot context.
- `backend/apps/classes/templates/classes/schedule.html` — "Prices" link per slot.
- `backend/tests/test_classes_classprice.py` — 35 tests referencing class_slot.
- `backend/apps/classes/migrations/0003_classprice_and_more.py` — migration that created ClassPrice with class_slot + constraint.
- Django 5.0 docs (Context7): `RemoveField` and `RemoveConstraint` migration operations.

## Decisions

### Decision 1: Use Django's auto-generated RemoveField + RemoveConstraint migration

**Decision**: Generate the migration via `python manage.py makemigrations classes`, which will auto-detect the removed `class_slot` field and the removed constraint, producing `RemoveField` and `RemoveConstraint` operations.

**Evidence**: Context7 docs confirm `migrations.RemoveField` removes a field from a model (reversible if nullable or has a default — `class_slot` is non-nullable, so the migration is irreversible, which is acceptable for this one-way refactoring). `migrations.RemoveConstraint` removes a constraint by its name (`unique_current_classprice_per_slot`).

**Rationale**: Auto-generation ensures the migration matches the model definition exactly, including dropping the partial unique index from PostgreSQL. Manual migration writing risks missing a dependency or constraint detail.

### Decision 2: Rework enter_price to create standalone current prices (no swap)

**Decision**: The `enter_price` classmethod is reworked to accept `(new_price, changed_by)` (no `class_slot`). Since there is no per-class current constraint, it simply creates a new `ClassPrice` with `current=True` — no previous-price retirement logic. The transaction and row-locking can be simplified (or kept for safety on the create).

**Evidence**: The spec (FR-006) says "reworked to not require a class_slot parameter — it must operate on standalone prices with no per-class current constraint." Without a per-class grouping, there is no "previous current price to archive." The `current` flag is retained on the model (FR-002) but multiple current prices may coexist.

**Rationale**: The atomic swap logic (retire previous current, create new current) only made sense in a per-class context. Without classes, each price entry is a new standalone record. Keeping the transaction context ensures atomicity of the create + any future audit stamping.

### Decision 3: Rework views to be global (not per-class)

**Decision**: `ClassPriceCreateView` no longer takes a `class_slot` pk from the URL. `ClassPricesView` lists all prices (not filtered by class_slot). URLs change from `classes/<int:pk>/prices/` to `prices/` and `prices/add/` (within the `classes` app namespace for now, or moved to a new `pricing` namespace — kept in `classes` app for minimal restructure).

**Evidence**: Without the class_slot association, prices are global entities. The views must display all prices, not per-class prices. The "Prices" link on the schedule page is removed (FR-008) since prices are no longer per-class.

**Rationale**: Keeping URLs in the `classes` app namespace minimizes structural change. The routes change from per-class (`classes/<pk>/prices/`) to global (`prices/`), but remain under `app_name = "classes"` since the `ClassPrice` model lives in the `classes` app.

### Decision 4: Remove class_slot from all templates

**Decision**: `class_prices.html` and `class_price_form.html` no longer reference `class_slot` context variables. The schedule page's "Prices" link is removed.

**Evidence**: Templates currently display `class_slot` info and link to per-class price pages. With the association removed, these references must be eliminated.

**Rationale**: Leaving dangling template references to `class_slot` would cause runtime errors (undefined variable) and broken links.

### Decision 5: Update tests to reflect decoupled model

**Decision**: Rewrite `backend/tests/test_classes_classprice.py` to test `ClassPrice` without `class_slot`. The `enter_price` signature changes; tests that pass `class_slot` are updated. Deletion-prevention tests are retained. Admin delete-permission test is updated.

**Evidence**: 25 of the 35 existing tests pass `class_slot` to the `class_slot` fixture or `enter_price()` call. These must be refactored. The 9 deletion-prevention and admin tests are mostly independent of class_slot.

**Rationale**: TDD requires tests to be written/updated first and FAIL before implementation. The test file must reflect the decoupled model before code changes.

### Decision 6: Keep ClassPrice entity name (not renamed to "Price")

**Decision**: The model remains named `ClassPrice` despite losing its class association. No rename is performed.

**Evidence**: Renaming would require a `RenameModel` migration and cascade of changes across admin, forms, views, tests, and i18n. The spec only asks to remove the association, not rename the entity. The `ClassSlotManager` (added in the current models.py as dead code during the 058 implementation) is also cleaned up.

**Rationale**: YAGNI — keep the refactoring minimal. Renaming can be a separate feature if/when the entity gains a different identity. The name `ClassPrice` is retained for backward compatibility of the DB table and app_label.

## Open Items

- None requiring clarification. All Technical Context unknowns resolved by source inspection and current Django documentation.
