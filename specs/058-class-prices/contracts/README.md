# Contracts: Class Price Versioning & Audit

This feature extends the `classes` app with a new `ClassPrice` model and a class-prices UI. The contracts below define the user-facing and data-layer interfaces that must not be broken by implementation.

## URL Route Contract

New routes added to the `classes` app (`backend/apps/classes/urls.py`, `app_name = "classes"`).

| Method | URL Pattern | View Name | Permission | Description |
|--------|-------------|-----------|------------|-------------|
| GET | `/classes/<int:pk>/prices/` | `classes:class-prices` | login required | Class prices history view: lists all price records (current + historical) for the slot, descending by `created_at`, with the active price flagged |
| POST | `/classes/<int:pk>/prices/add/` | `classes:class-price-add` | Administrator (superuser or `Administrators` group) | Enter a new current price for the slot; atomically retires the previous current price |
| — | Django admin | `admin:classes_classprice_*` | Staff | Read-only browsing; delete disabled |

No existing routes are modified or removed. `classes/` (schedule) and `classes/<int:pk>/toggle/` remain unchanged. A "Prices" link is added on the schedule row for each slot.

## Template Context Contract

### `classes/class_prices.html`

| Variable | Type | Meaning |
|----------|------|---------|
| `class_slot` | `ClassSlot` | The class whose prices are shown |
| `current_price` | `ClassPrice` or `None` | The single active (`current=True`) price, or None if no price has ever been set |
| `price_history` | QuerySet[ClassPrice] | All prices for the slot, ordered by `-created_at` (most recent first) |
| `user_can_add` | bool | True if the acting user is an administrator (drives the "Add price" button) |

### `classes/schedule.html` (modified)

A "Prices" link (`{% url 'classes:class-prices' slot.pk %}`) is rendered per active schedule row, guarded by `perms.classes.view_classprice` when the permission is added by the new model's `Meta`.

## i18n Contract

All user-visible strings are internationalized. New Spanish (`es`) translations added to `backend/locale/es/LC_MESSAGES/django.po` and compiled to `messages.mo`:

| English source string | Usage |
|-----------------------|-------|
| Class Prices | Page heading / nav label |
| Current | Badge/label on the active price |
| Inactive | Label on historical prices |
| Price | Column / form label |
| Effective | Column header (creation/effective date) |
| Superseded | Column header (change date) |
| Created by | Column header |
| Changed by | Column header |
| Add price | Button (admin only) |
| Enter a new price | Form heading |
| This class has no price history. | Empty state |
| A current price already exists. Updating it will archive the previous price. | Confirmation notice |
| Prices cannot be deleted. | Error message on delete attempt |
| Enter a positive amount. | Validation message |

## Data-Layer / Model Contract

- `ClassPrice` is registered in the `classes` app (app_label `classes`); migration is `classes/0003_classprice.py`.
- `class_slot` FK uses `on_delete=PROTECT` (`ClassSlot` deletion is blocked while price history exists).
- `created_by`/`changed_by` FKs use `on_delete=PROTECT` (admins/users are never cascade-removed).
- The filtered unique constraint named `unique_current_classprice_per_slot` MUST exist after migration.
- `delete()` is overridden to raise `ProtectedError` (or equivalent) so no code path can delete a `ClassPrice`.
- QuerySet `delete()` is also blocked (override) so bulk deletion fails with a clear error.
