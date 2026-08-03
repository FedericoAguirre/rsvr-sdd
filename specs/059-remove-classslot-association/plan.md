# Implementation Plan: Remove ClassPrice-ClassSlot Association

**Branch**: `059-remove-classslot-association` | **Date**: 2026-08-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/059-remove-classslot-association/spec.md`

## Summary

Refactor the `ClassPrice` model to remove the `class_slot` ForeignKey association, because no business rule currently links class prices to class slots. All dependent assets — model, migration, admin, views, forms, URLs, templates, tests, and i18n — are adjusted to treat `ClassPrice` as a standalone entity. The versioning, audit, and deletion-prevention features from `058-class-prices` are preserved; only the class-slot coupling is removed.

## Technical Context

**Language/Version**: Python 3.13 / Django 5.0.14 (project requires `>=3.12`, ruff target `py312`)

**Primary Dependencies**: Django 5.0.14 (ORM, admin, auth), psycopg2-binary, pytest + pytest-django, Bootstrap 5.3.3, ruff (all existing; no new dependencies)

**Storage**: PostgreSQL 16 (Docker)

**Testing**: pytest via `make test` (`cd backend && uv run pytest`); lint via `make lint` (`cd backend && uv run ruff check .`); format via `make format`

**Target Platform**: Linux server, Docker Compose (db service) + native `uv run manage.py` dev server

**Project Type**: Web application (Django), single backend project with app-based separation under `backend/apps/`

**Performance Goals**: Price list view renders from a single indexed query (all prices, ordered by `-created_at`); target < 2s page load per spec SC-002. Attribution joined via `select_related("created_by", "changed_by")`.

**Constraints**:
- All user-visible strings MUST remain internationalized (Constitution Principle III.i18n).
- `enter_price` MUST be reworked to not require `class_slot` — creates a standalone current price without per-class swap logic.
- Price records MUST NEVER be deleted: model `delete()` overridden, queryset `delete()` overridden, admin `has_delete_permission=False`, `on_delete=PROTECT` on user FKs.
- Only authorized administrators may create prices (reuse `UserPassesTestMixin` + `Administrators` group pattern).
- Historical price values immutable; only status fields (`current`, `changed_at`, `changed_by`, `updated_at`) are writable on retire.
- Migration MUST cleanly remove the `class_slot` column and the `unique_current_classprice_per_slot` constraint (Django `RemoveField` + `RemoveConstraint` operations, confirmed via Context7 docs).

**Scale/Scope**: Small refactoring — remove one FK and one constraint from the existing `ClassPrice` model, rework 3 views/templates/URLs, update tests and i18n. No new apps or dependencies.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **I. Code Quality** | ✅ PASS | Removing a premature FK and its constraint reduces coupling; no dead code introduced; `ruff check` + `ruff format` required. |
| **II. Testing Standards** | ✅ PASS | TDD: tests updated first to reflect decoupled model (no class_slot), confirmed RED, then implementation; deletion-prevention tests retained; Constitution Principle II — integration tests cover the migration and view changes. |
| **III. UX Consistency (i18n)** | ✅ PASS | All remaining user-visible strings use `{% translate %}` / `gettext_lazy`; Spanish `.po`/`.mo` updated and compiled; verified at runtime. |
| **IV. Performance** | ✅ PASS | Price list view uses a single indexed query (no class_slot filter); SC-002 (<2s) target unchanged; no N+1 via `select_related`. |
| **V. External Docs** | ✅ PASS | Django 5.0.14 migration operations (`RemoveField`, `RemoveConstraint`) confirmed via Context7 docs (`/django/django`). No new dependencies. |

## Project Structure

### Documentation (this feature)

```text
specs/059-remove-classslot-association/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 — research artifacts
├── data-model.md        # Phase 1 — entity definitions
├── quickstart.md        # Phase 1 — development quickstart
└── tasks.md             # Phase 2 — implementation tasks (generated later)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── classes/
│       ├── models.py          # MODIFY: remove class_slot FK + constraint from ClassPrice
│       ├── admin.py           # MODIFY: remove class_slot from ClassPriceAdmin
│       ├── views.py           # MODIFY: rework ClassPriceCreateView + ClassPricesView (no class_slot context)
│       ├── urls.py            # MODIFY: change routes to prices/ and prices/add/ (no class pk)
│       ├── forms.py           # MODIFY: ClassPriceForm (no class_slot-dependent fields)
│       ├── templates/classes/
│       │   ├── schedule.html       # MODIFY: remove "Prices" link
│       │   ├── class_prices.html    # MODIFY: remove class_slot context
│       │   └── class_price_form.html  # MODIFY: remove class_slot context
│       └── migrations/
│           └── 0004_remove_classprice_class_slot.py  # NEW: RemoveField + RemoveConstraint
└── tests/
    └── test_classes_classprice.py  # REWRITE: tests for decoupled ClassPrice
```

**Structure Decision**: Refactoring lives entirely within the existing `classes` app (where `ClassPrice` was introduced in `058-class-prices`). The `ClassPrice` model, its admin registration, views, URLs, templates, and tests are all adjusted in-place. A new migration (`0004`) removes the `class_slot` field and the filtered unique constraint.

## Complexity Tracking

> No constitution violations to justify. Feature is a small refactoring: removing one FK and one constraint, reworking views/URLs/templates to be global (not per-class), and updating tests. The `ClassPrice` entity and its audit/deletion-prevention invariants are unchanged.
