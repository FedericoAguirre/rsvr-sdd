# Research: Class Price Versioning & Audit

**Date**: 2026-08-02
**Spec**: `specs/058-class-prices/spec.md`
**Plan**: `specs/058-class-prices/plan.md`

## Purpose

Resolve every unknown in the plan's Technical Context so that the data model and implementation contracts are grounded in the actual application, and validate the ORM/transactional design decisions against current Django 5.0 documentation (Constitution Principle V).

## Method

Read-only inspection of the current application source plus authoritative Django documentation fetched via Context7 (library ID `/django/django`).

- `backend/apps/classes/models.py` — `ClassSlot` entity (the only "class" model; no `Class` model exists).
- `backend/apps/payments/models.py` — attribution pattern (`created_by`/`updated_by` FK to `AUTH_USER_MODEL`), soft-delete pattern, `transaction.atomic` usage.
- `backend/apps/payments/views.py` — admin-guard pattern (`UserPassesTestMixin`, `Administrators` group), batch atomic creation (`select_for_update` context).
- `backend/apps/classes/admin.py`, `classes/urls.py`, `classes/views.py`, `classes/templates/classes/schedule.html` — existing class UI patterns.
- `backend/config/urls.py` and `backend/templates/base.html` — route table and navigation.
- `backend/locale/es/LC_MESSAGES/django.po` — canonical Spanish UI labels and `{% translate %}` conventions.
- `pyproject.toml` / `.specify/integration.json` / `Makefile` — versions, tools, test commands.
- Django 5.0 docs (Context7): conditional `UniqueConstraint(condition=Q(...))`, `transaction.atomic`, `select_for_update(of=("self",))`, overriding model `delete()`, and `Collector` deletion semantics (`PROTECT`).

## Decisions

### Decision 1: "class" maps to `ClassSlot` (resolves NEEDS CLARIFICATION)

**Decision**: The spec's `class_id` refers to the existing `ClassSlot` model; a new `Class` entity is NOT introduced.

**Evidence**:
- The `classes` app contains only `ClassSlot` (fields `day_of_week`, `time`, `is_active`); there is no `Class` model anywhere in `backend/apps/`.
- `Reservation` references `ClassSlot` (not a `Class`); payments count `class_slot_count` slots.
- A grep for `classprice`, `class_price`, `precio`/`price` across `backend/apps` returns **zero** matches → no existing price model to extend or reuse.

**Rationale**: Pricing attaches to the same entity reservations and payments already key on (`class_slot`), keeping a single source of truth for "a class". Introducing a parallel `Class` concept would split the domain and require re-wiring reservations/payments.

**Alternatives considered**:
- Creating a new `Class` (course-type) entity above `ClassSlot` — rejected: no demand in the spec; would be speculative scope expansion and a large data-model change.

### Decision 2: Enforced single current price via filtered UniqueConstraint (resolves NEEDS CLARIFICATION)

**Decision**: Enforce "exactly one current price per class" with a database-level filtered unique constraint:

```python
models.UniqueConstraint(
    fields=["class_slot"], condition=Q(current=True),
    name="unique_current_classprice_per_slot",
)
```

**Evidence**: Django docs confirm `UniqueConstraint` accepts a `condition` `Q` object ("Constraints reference > UniqueConstraint > condition"), producing a partial unique index so that **only one row with `current=True` may exist per `class_slot`** while multiple inactive historical rows are allowed. This is the canonical, database-enforced way to express "single active record per parent".

**Rationale**: A pure application-level check would be race-prone under concurrent admin changes; the constraint is the durable guarantee the spec's AC-008 ("only one current price exists per class") requires, backed by the atomic swap in Decision 4.

**Alternatives considered**:
- Application-only check in the view/service — rejected: not concurrency-safe; the constitution's data-integrity requirement demands a DB-level guarantee.

### Decision 3: Hard deletion prevention, not soft-delete (resolves NEEDS CLARIFICATION)

**Decision**: Price records are **hard-prevented** from deletion (overriding `Model.delete()` to raise, admin `has_delete_permission=False`, and `on_delete=PROTECT` on the FK). A soft-delete flag is NOT used.

**Evidence**: The spec explicitly states "Class prices cannot be deleted from the database", "Deletion attempts must fail with a clear error message", and "All historical price records remain immutable". Django's `Collector.delete()` wraps deletes in `transaction.atomic` and raises `ProtectedError` when a `PROTECT` FK blocks it; overriding `delete()` is the documented hook for custom deletion logic.

**Rationale**: The spec's intent is total non-loss of history. The project's own `Payment` model uses soft-delete (`is_deleted`/`deleted_at`) for a different lifecycle (payments can be "removed" from active lists but retained); here the spec demands stronger protection — no logical deletion path at all. Reusing the soft-delete pattern would contradict "cannot be deleted" and "immutable".

**Alternatives considered**: Reusing `is_deleted`/`deleted_at` soft-delete — rejected: conflicts with the explicit, stronger spec requirement and the immutability requirement.

### Decision 4: Atomic retire-and-create swap with row locking

**Decision**: Enter price via a single `@transaction.atomic` block that (a) selects the current price for the slot with `select_for_update(of=("self",))`, (b) sets it `current=False` with `changed_at`/`changed_by`, then (c) creates the new `current=True` record — capturing `created_by` on the new record.

**Evidence**: Django docs confirm `transaction.atomic` makes the block all-or-nothing, and `select_for_update(of=("self",))` is the documented row-locking pattern to serialize concurrent writers. The existing `BatchCreateView` already uses `transaction.atomic` for reservation creation, so this aligns with the project's concurrency style. The filtered unique constraint (Decision 2) makes the swap safe even if locking were bypassed.

**Rationale**: Without atomicity, a crash between retiring the old price and creating the new one would leave a class with no current price. Row locking prevents the lost-update race where two admins both retire the same price and both insert a new current price.

### Decision 5: Attribution follows the `Payment` pattern

**Decision**: `ClassPrice` includes `created_by` (FK to `AUTH_USER_MODEL`, the user who entered the price) and `changed_by` (FK, nullable, the user who retired it) plus `changed_at` (nullable). `created_at` (auto_now_add) is the effective date; `updated_at` (auto_now) tracks last touch.

**Evidence**: `Payment` uses `created_by` + `updated_by` FKs to `AUTH_USER_MODEL` with `on_delete=PROTECT` and the admin `save_model` override stamps the acting user. The spec AC requires "change metadata (who, when) when superseded", which the `class_id`/`price`/`current`/`created_by`/`created_at`/`changed_at`/`updated_at` column list does not enumerate a changer FK for — so `changed_by` is added to satisfy the audit AC, consistent with `Payment.updated_by`.

**Rationale**: Reusing the proven attribution shape keeps the model and admin code consistent with `Payment`; `changed_by` is explicitly required by AC "who [retired] the price".

### Decision 6: Prices UI lives in the `classes` app

**Decision**: The "class prices view page" is a new view in the `classes` app: `classes/<int:pk>/prices/` (`classes:class-prices`, login-required), with a POST route to add a price restricted to administrators. `schedule.html` gains a per-slot "Prices" link.

**Evidence**: `ClassSlot` and its management views/admin live in the `classes` app; the nav (`base.html`) already guards `classes:class-schedule` with `perms.classes.view_classslot`. A prices page is the natural extension path from the schedule.

**Rationale**: Keeps price management co-located with the class it prices; avoids creating a new top-level module.

**Alternatives considered**: Managing prices only through Django admin — rejected: the spec requires a user-facing "class prices view page" showing descending history with a current-price flag, which is a UI concern, not raw admin.

### Decision 7: i18n follows existing conventions

**Decision**: Models use `gettext_lazy` for `verbose_name`/`__str__`; templates use `{% load i18n %}` and `{% translate %}`; new strings are added to `backend/locale/es/LC_MESSAGES/django.po` and compiled (`messages.mo`) so the Spanish UI is verified, per Constitution Principle III.i18n.

**Evidence**: The codebase consistently uses `gettext_lazy as _` and `{% translate %}` (e.g., `schedule.html`, `ClassSlot.__str__`); the constitution mandates Spanish output verification before merge.

### Decision 8: Test/lint commands reused from Makefile

**Decision**: Tests run via `make test` (`cd backend && uv run pytest`); lint/format via `make lint`/`make format`. New tests go in `backend/tests/test_classes_classprice.py`.

**Rationale**: Matches the documented, constitution-mandated verification path.

## Open Items

- None requiring clarification. All Technical Context unknowns resolved by source inspection and current Django documentation.
