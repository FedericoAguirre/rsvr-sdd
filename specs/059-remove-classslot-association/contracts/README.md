# Contracts: Remove ClassPrice-ClassSlot Association

This feature refactors the `ClassPrice` model to remove the `class_slot` ForeignKey. The contracts below define the user-facing and data-layer interfaces that must not be broken by implementation.

## URL Route Contract

### Removed Routes (from 058-class-prices)

| Method | URL Pattern | View Name | Action |
|--------|-------------|-----------|--------|
| GET | `/classes/<int:pk>/prices/` | `classes:class-prices` | **Removed** — per-class prices view no longer applies |
| POST | `/classes/<int:pk>/prices/add/` | `classes:class-price-add` | **Removed** — per-class price add no longer applies |

### New Routes (global prices)

| Method | URL Pattern | View Name | Permission | Description |
|--------|-------------|-----------|------------|-------------|
| GET | `/prices/` | `classes:price-list` | login required | Price history view: lists all price records globally, ordered by `-created_at`, with current prices flagged |
| POST | `/prices/add/` | `classes:price-add` | Administrator | Enter a new standalone price; no class_slot context |
| — | Django admin | `admin:classes_classprice_*` | Staff | Read-only browsing; delete disabled |

### Removed from schedule.html

The "Prices" link previously added per-slot in `classes/templates/classes/schedule.html` is **removed** (FR-008). The schedule page returns to its pre-`058` state.

## Template Context Contract

### `classes/class_prices.html` (rewritten)

| Variable | Type | Meaning |
|----------|------|---------|
| `current_prices` | QuerySet[ClassPrice] | All current (`current=True`) prices |
| `price_history` | QuerySet[ClassPrice] | All prices, ordered by `-created_at` |
| `user_can_add` | bool | True if the acting user is an administrator |

**`class_slot`**: No longer in context (removed).

### `classes/class_price_form.html` (rewritten)

| Variable | Type | Meaning |
|----------|------|---------|
| `form` | `ClassPriceForm` | Form with only the `price` field |
| `current_prices` | QuerySet[ClassPrice] | For display in the confirmation notice |

**`class_slot`** and **`current_price`**: No longer in context (removed).

### `classes/schedule.html` (modified)

The "Prices" column/link is **removed**. Returns to original 3-column layout.

## i18n Contract

All user-visible strings remain internationalized. New/modified strings in `backend/locale/es/LC_MESSAGES/django.po`:

| English source string | Usage |
|-----------------------|-------|
| Price list | Page heading for global prices view |
| No price history exists yet. | Empty state (was "This class has no price history.") |
| Current | Badge on active prices |
| Inactive | Badge on retired prices |
| Price | Column/form label |
| Effective | Column header (creation date) |
| Superseded | Column header (change date) |
| Created by | Column header |
| Changed by | Column header |
| Add price | Button (admin only) |
| Enter a new price | Form heading |
| Save | Button |
| Cancel | Button |
| Prices | Nav link (was per-class, now global) |
| Price updated successfully. | Success message |
| Enter a positive amount. | Validation message |
| Class price records cannot be deleted. | Error message on delete attempt |

## Data-Layer / Model Contract

- `ClassPrice` is registered in the `classes` app (app_label `classes`); migration `classes/0004_remove_classprice_class_slot.py`.
- `class_slot` FK is **removed** — migration uses `migrations.RemoveField`.
- The filtered unique constraint `unique_current_classprice_per_slot` is **removed** — migration uses `migrations.RemoveConstraint`.
- `created_by`/`changed_by` FKs retain `on_delete=PROTECT`.
- `delete()` remains overridden to raise `PermissionDenied`; admin `has_delete_permission=False`.
- `enter_price` signature changes from `enter_price(class_slot, new_price, changed_by)` to `enter_price(new_price, changed_by)` — creates a standalone current price, no per-class swap.
