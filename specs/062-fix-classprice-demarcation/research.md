# Research: Fix ClassPrice Demarcation

**Feature**: 062-fix-classprice-demarcation
**Date**: 2026-08-02

## Research Task: How to retire previous current prices in `enter_price()`

### Decision

Modify `ClassPrice.enter_price()` to bulk-update all existing `current=True` records to `current=False` with `changed_at=timezone.now()` and `changed_by=changed_by` **before** creating the new price — all within the existing `transaction.atomic()` block.

### Rationale

The fix is tightly scoped:

1. **Location**: `ClassPrice.enter_price()` at `backend/apps/classes/models.py:141-148` is the single entry point for all price creation (used by both the view and the manager). Fixing it here fixes the bug everywhere.

2. **Approach**: Use `cls.objects.filter(current=True).update(current=False, changed_at=timezone.now(), changed_by=changed_by)` — a single bulk UPDATE query. This is the most efficient approach and avoids N+1 SELECT + individual saves.

3. **Atomicity**: The `transaction.atomic()` decorator is already on the classmethod. Adding the update before the create ensures both operations succeed or both roll back.

4. **Import needed**: `from django.utils import timezone` — not currently imported in `models.py`, must be added.

5. **No migration**: No schema changes. All fields involved (`current`, `changed_at`, `changed_by`) already exist and are nullable where appropriate.

6. **Edge case — first price**: If no `current=True` records exist (first price in the system), `filter(...).update()` updates zero rows silently — no side effects.

7. **Edge case — multiple current prices**: The bulk update hits all `current=True` records regardless of count, addressing the pre-fix legacy state automatically.

### Alternatives Considered

| Alternative | Rejected Because |
|---|---|
| Iterate and `.save()` each record individually | N+1 queries; breaks atomicity if not wrapped; unnecessary |
| Django signal (`pre_save`/`post_save`) | Adds indirection; harder to test; not needed for a single-method fix |
| Data migration to clean existing duplicates | Unnecessary — `filter(...).update()` handles all `current=True` records at once on the next price entry |
| Add a unique constraint on `current=True` | Would require cleanup of existing data; over-engineering for this fix |
