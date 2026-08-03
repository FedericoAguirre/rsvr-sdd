# Implementation Plan: Class Price Versioning & Audit

**Branch**: `058-class-prices` | **Date**: 2026-08-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/058-class-prices/spec.md`

## Summary

Add versioned, audit-trail-backed class pricing to the RSVR application. A new `ClassPrice` model in the `classes` app tracks each price change for a `ClassSlot` (the project's "class" entity — a recurring weekly slot such as "Monday 17:30"), preserving the previous price as inactive with full who/when attribution whenever a new current price is entered. Price records can never be deleted, and only one active (`current`) price may exist per class at any time. A new class prices view page surfaces the full history in descending chronological order with the active price clearly flagged.

The technical approach reuses the project's established patterns: the `created_by`/`updated_by` FK-to-user attribution (cf. `Payment`), `transaction.atomic` with row locking for the atomic retire-and-create swap (cf. `BatchCreateView`), i18n via `gettext_lazy`/`{% translate %}`, and a filtered `UniqueConstraint(condition=Q(current=True))` to enforce a single current price per class. No new dependencies are introduced.

## Technical Context

**Language/Version**: Python 3.13 (runtime; project requires `>=3.12`, ruff target `py312`), Django 5.0.14

**Primary Dependencies**: Django 5.0 (ORM, admin, auth), psycopg2-binary, pytest + pytest-django, Bootstrap 5.3.3, HTMX 2.0.4, openpyxl, ReportLab, icalendar, pdfminer-six (all existing; no new dependencies)

**Storage**: PostgreSQL 16 (Docker)

**Testing**: pytest via `make test` (`cd backend && uv run pytest`); lint via `make lint` (`ruff check .`); format via `make format`

**Target Platform**: Linux server, Docker Compose (db service) + native `uv run manage.py` dev server

**Project Type**: Web application (Django), single backend project with app-based separation under `backend/apps/`

**Performance Goals**: Class prices view renders from a single indexed query (filter by `class_slot`, ordered by `-created_at`); target < 2s page load per spec SC-002. Attribution joined via `select_related("created_by", "changed_by")` to avoid N+1.

**Constraints**:
- All new user-visible strings MUST be internationalized via `{% translate %}` / `gettext_lazy` (Constitution Principle III.i18n — NON-NEGOTIABLE).
- Only one active price per class: enforced by a filtered `UniqueConstraint(fields=["class_slot"], condition=Q(current=True))`.
- Price change MUST be atomic: retire previous current price (`current=False`, `changed_at`, `changed_by`) and create the new current price within one `transaction.atomic` block, locking the relevant rows with `select_for_update(of=("self",))` to handle concurrent admin changes (cf. Django docs: filtered `UniqueConstraint`, `transaction.atomic`, `select_for_update`).
- Price records MUST NEVER be deleted: model `delete()` is overridden to raise, admin `has_delete_permission` is disabled, and `on_delete=PROTECT` guards the FK — hard prevention, NOT soft-delete (per spec "cannot be deleted from the database"; the existing `Payment` soft-delete pattern is deliberately NOT reused here).
- Only authorized administrators may enter/change prices (reuse `Administrators` group / `UserPassesTestMixin` pattern from `PaymentExportView`/`PaymentReportView`).
- Historical price values and creation metadata are immutable; when a price is retired, only status fields (`current`, `changed_at`, `changed_by`, `updated_at`) are written — never the `price` amount or `created_*` fields.

**Scale/Scope**: Small feature — new `ClassPrice` model + migration in `classes` app, one new prices view + route + template, admin registration, and a focused test module. No schema changes to existing models; no new apps.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **I. Code Quality** | ✅ PASS | New model + view; no dead code/duplication; follows existing `ClassSlot`/`Payment` patterns; `ruff check` + `ruff format` required. |
| **II. Testing Standards** | ✅ PASS | TDD: tests for atomic version swap, single-current constraint, deletion prevention, view ordering/flagging, empty state. Red-Green-Refactor enforced; new DB contract tested. |
| **III. UX Consistency (i18n)** | ✅ PASS | All new strings (view heading, empty state, audit labels, admin, prices column) via `{% translate %}`/`gettext_lazy`; Spanish `.po`/`.mo` updated and compiled. |
| **IV. Performance** | ✅ PASS | Single indexed query for prices view; SC-002 (<2s) is the measurable target; no N+1 via `select_related`. |
| **V. External Docs** | ✅ PASS | Django 5.0.14 ORM patterns (filtered `UniqueConstraint`, `transaction.atomic`, `select_for_update`, overriding `delete()`) confirmed against current Django docs via Context7. No new dependencies. |

## Project Structure

### Documentation (this feature)

```text
specs/058-class-prices/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 — research artifacts
├── data-model.md        # Phase 1 — entity definitions
├── quickstart.md        # Phase 1 — development quickstart
├── contracts/           # Phase 1 — interface contracts
│   └── README.md        # Routes, template context, and i18n contracts
└── tasks.md             # Phase 2 — implementation tasks (generated later)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── classes/
│       ├── models.py              # NEW: ClassPrice model added
│       ├── admin.py               # MODIFY: register ClassPrice (delete disabled)
│       ├── views.py               # NEW: ClassPricesView + ClassPriceCreateView
│       ├── urls.py                # MODIFY: add classes/<int:pk>/prices/ routes
│       ├── forms.py               # NEW: ClassPriceForm
│       └── templates/classes/
│           ├── schedule.html      # MODIFY: add Prices link per slot
│           └── class_prices.html  # NEW: price history view
└── tests/
    └── test_classes_classprice.py # NEW: versioning, uniqueness, deletion tests
```

**Structure Decision**: Django web application — single backend project with app-based separation. The feature lives entirely within the existing `classes` app (where `ClassSlot` is defined): the `ClassPrice` model, its admin registration, a new prices view/route/template, and tests. No new apps or utilities are needed. The "class" priced by this feature is the existing `ClassSlot` ("bloque de clase"), so `ClassPrice` references `ClassSlot` via FK. No new migration app label is required.

## Complexity Tracking

> No constitution violations to justify. Feature is small: one new model with a filtered unique constraint, a new view reusing the existing `LoginRequiredMixin` + admin-guard pattern, and focused tests.
