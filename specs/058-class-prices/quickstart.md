# Quickstart Validation: Class Price Versioning & Audit

**Date**: 2026-08-02
**Spec**: `specs/058-class-prices/spec.md`
**Plan**: `specs/058-class-prices/plan.md`
**Contract**: `contracts/README.md`
**Data model**: `data-model.md`

## Purpose

Runnable validation scenarios that prove the feature works end-to-end: versioned pricing, single-current enforcement, deletion prevention, and correct UI ordering/flagging. Validation is primarily automated (pytest) with one manual UI check.

## Prerequisites

- A checkout of the repository on branch `058-class-prices`.
- Database at `localhost:5432` with the `rsvr` role (e.g., `make db-up`); migrations applied (`make migrate`).
- Demo/class data: `make seed` provides ClassSlots; create an admin user with `make createsuperuser` (assign to `Administrators`).
- Python test tooling installed via `uv` (per the constitution). Run tests with `make test`; lint with `make lint`.

## Scenario 1 — First price becomes the current price

**GIVEN** a `ClassSlot` that has never had a price,
**WHEN** an administrator enters a price,
**THEN**:

- [ ] A `ClassPrice` is created with `current=True`, `changed_at=None`, `created_by` set, `class_slot` set.
- [ ] `ClassPrice.objects.filter(class_slot=slot, current=True).count() == 1`.

## Scenario 2 — Updating a price archives the previous one (FR-001/002/003)

**GIVEN** a slot with a current price P1,
**WHEN** an administrator enters a new price P2,
**THEN** (all within one transaction):

- [ ] P1 is now `current=False` with `changed_at` and `changed_by` populated.
- [ ] P1's `price` amount is unchanged.
- [ ] P2 is `current=True`, `created_by` set, `changed_at=None`.
- [ ] Exactly one `current=True` price exists for the slot.
- [ ] The change is atomic: if the new price save fails, P1 remains `current=True` (no gap).

## Scenario 3 — Single current price enforced (FR-009)

**GIVEN** a slot with a current price,
**WHEN** a second current price is inserted directly (bypassing the service),
**THEN**:

- [ ] The DB raises an `IntegrityError` due to `unique_current_classprice_per_slot`.

## Scenario 4 — Deletion is prevented (FR-008)

**GIVEN** a slot with current and historical prices,
**WHEN** an administrator attempts to delete any `ClassPrice` (ORM, admin, or view),
**THEN**:

- [ ] The operation raises an error and the record remains `count == unchanged`.
- [ ] No price record (active or historical) is ever removed.

## Scenario 5 — History view ordering and current flag (FR-006/007)

**GIVEN** a slot that was re-priced several times,
**WHEN** an administrator opens `/classes/<pk>/prices/`,
**THEN**:

- [ ] Records appear in descending `created_at` order.
- [ ] The active price carries a visible "Current" badge.
- [ ] Every row shows `price`, effective (`created_at`), superseded (`changed_at`), creator, and changer.
- [ ] The empty state "This class has no price history." renders when no prices exist.

## Scenario 6 — Administrator-only changes (FR-011)

**GIVEN** a non-administrator (logged-in but not superuser/`Administrators`),
**WHEN** visiting `/classes/<pk>/prices/add/` or POSTing a new price,
**THEN**:

- [ ] The request is denied (403) and no `ClassPrice` is created.

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

All checkboxes above must pass. Failure on any of Scenarios 1–4 indicates a data-integrity or atomicity defect; Scenario 5 a UI/ordering defect; Scenario 6 an access-control defect. Any failure blocks `/speckit.tasks`.
