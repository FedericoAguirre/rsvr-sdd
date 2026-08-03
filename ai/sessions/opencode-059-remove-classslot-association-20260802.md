# Session: Remove ClassPrice-ClassSlot Association

## Feature
059-remove-classslot-association — Remove the `class_slot` ForeignKey from the `ClassPrice` model to fully decouple pricing from class scheduling. Pricing records are now standalone and global; a price can be entered for any `ClassPrice` without depending on a `Class` or `ClassSlot`.

## Workflow
/speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.implement

## Spec (via specs/059-remove-classslot-association/)
US1: ClassPrice no longer depends on ClassSlot. `enter_price` creates a standalone current price record and prevents duplicate current prices.

## Changes
- backend/apps/classes/models.py: Removed `class_slot` FK, `unique_current_classprice_per_slot` constraint; rewrote `enter_price` as standalone (no swap/retire); removed dead `ClassSlotManager`; simplified `__str__` to `"%(price)s"` only; removed unused `datetime` import.
- backend/apps/classes/migrations/0004_remove_classprice_class_slot.py: new migration (RemoveConstraint + RemoveField).
- backend/apps/classes/admin.py: Removed `class_slot` from `ClassPriceAdmin` list_display/search_fields/readonly_fields.
- backend/apps/classes/views.py: `ClassPriceCreateView` reworked (admin-only, calls `enter_price`, redirects to price-list); `ClassPricesView` reworked (global list with `current_prices`/`price_history`/`user_can_add` context).
- backend/apps/classes/urls.py: Routes changed from `classes/<int:pk>/prices/` → `classes/prices/` (price-list) and `classes/prices/add/` (price-add).
- backend/apps/classes/templates/classes/class_prices.html: Global price table with current/current prices badges, no class_slot context.
- backend/apps/classes/templates/classes/class_price_form.html: Standalone price entry (no class_slot context, shows current prices warning).
- backend/apps/classes/templates/classes/schedule.html: Removed "Prices" column/link per slot (3-column layout restored).
- backend/tests/test_classes_classprice.py: 35 tests rewritten → 34 tests for decoupled model (TDD: RED→GREEN).
- backend/locale/es/LC_MESSAGES/django.po + .mo: Updated 5 Spanish translations for new/modified strings, all fuzzy flags removed.

## Notes
- 320 tests pass (was 321 baseline; original 35 ClassPrice tests rewritten to 34 decoupled tests).
- No `class_slot` references in any ClassPrice code path.
- Spanish i18n compiled with no fuzzy entries.
- Lint: No new error types introduced (only pre-existing D-docstring violations across codebase).
- All implementation committed as `[Spec Kit] Implementation progress` (squash pending).
