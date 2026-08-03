# Quickstart Validation: Remove ClassPrice-ClassSlot Association

**Date**: 2026-08-02
**Spec**: `specs/059-remove-classslot-association/spec.md`
**Plan**: `specs/059-remove-classslot-association/plan.md`

## Purpose

Runnable validation scenarios that prove the refactoring works: `ClassPrice` no longer has a `class_slot` FK, all dependent code works without it, and the existing features (versioning, audit, deletion prevention, i18n) remain intact.

## Prerequisites

- Checkout of the repository on branch `059-remove-classslot-association`.
- Database at `localhost:5432` with the `rsvr` role (e.g., `make db-up`).
- Apply migrations: `make migrate`.
- Python test tooling installed via `uv`. Run tests with `make test`; lint with `make lint`.

## Scenario 1 — ClassPrice model has no class_slot field

**GIVEN** the `ClassPrice` model,
**WHEN** introspection is performed,
**THEN**:

- [ ] `ClassPrice` has no attribute `class_slot`
- [ ] The migration `0004` exists with `RemoveField` for `class_slot` and `RemoveConstraint` for `unique_current_classprice_per_slot`

## Scenario 2 — enter_price creates standalone current price

**GIVEN** an admin user,
**WHEN** `ClassPrice.objects.enter_price(new_price=150.00, changed_by=admin)` is called,
**THEN**:

- [ ] A `ClassPrice` is created with `current=True`, `created_by=admin`, `changed_at=None`
- [ ] No `IntegrityError` from missing `class_slot`

## Scenario 3 — Price list view shows all prices

**GIVEN** multiple `ClassPrice` records,
**WHEN** an admin opens `/prices/`,
**THEN**:

- [ ] All prices are displayed in descending `created_at` order
- [ ] The active price carries a visible "Current" badge (Spanish: "Actual")

## Scenario 4 — Deletion still prevented

**GIVEN** a `ClassPrice` record,
**WHEN** an admin attempts to delete it (instance, queryset, or admin),
**THEN**:

- [ ] The operation raises an error and the record remains

## Scenario 5 — Schedule page has no Prices link

**GIVEN** the class schedule page,
**WHEN** viewing any class slot row,
**THEN**:

- [ ] No "Prices" link or button is present

## Scenario 6 — i18n intact

**GIVEN** the prices list page,
**WHEN** viewing as a Spanish-locale user,
**THEN**:

- [ ] All user-visible strings render in Spanish (no raw English strings visible)

## Run Commands

```bash
# Apply migrations (after implementation)
make migrate

# Run the feature's tests
cd backend && uv run pytest tests/test_classes_classprice.py -v

# Run full suite + lint
make test
make lint
make format
```

## Expected Outcomes

All checkboxes above must pass. Scenario 1 validates the model change; Scenario 2 the service rework; Scenario 3 the view/template rework; Scenario 4 confirms deletion prevention is retained; Scenario 5 confirms schedule cleanup; Scenario 6 confirms i18n.
