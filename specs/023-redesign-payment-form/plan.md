# Implementation Plan: Payment Form Redesign

**Branch**: `023-redesign-payment-form` | **Date**: 2026-06-24 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/023-redesign-payment-form/spec.md`

## Summary

Redesign the payment creation/edit form to match the project's established Django form conventions. Two changes are required: (1) update the template field wrappers from `col-12` to `col-md-6`, matching client/equipment/reservation forms; (2) add `"class": "form-control"` to all widget attrs in `PaymentForm.Meta.widgets`, ensuring consistent Bootstrap 5 input styling. All existing validation, edit-mode field locking, evidence upload, and CSRF handling must be preserved with zero behavioral changes.

## Technical Context

**Language/Version**: Python 3.12, Django 5.0.x

**Primary Dependencies**: Django 5.0, Bootstrap 5 (via CDN), HTMX, psycopg2-binary for PostgreSQL

**Storage**: PostgreSQL

**Testing**: pytest 9.1.0 + pytest-django; Django TestClient for view/integration tests

**Target Platform**: Linux server (deployed via Gunicorn + Whitenoise)

**Project Type**: Web application (Django monolith with Bootstrap 5 frontend)

**Performance Goals**: N/A — visual/structural change only

**Constraints**: Must match existing form patterns exactly; no behavioral changes permitted; i18n strings must not be altered; existing test suite (292 lines across 14 test classes) must continue passing

**Scale/Scope**: 2 files modified (`forms.py`, `payment_form.html`); 1 file for new tests (`test_payments.py`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Testing Standards (TDD — Non-Negotiable)

**Status**: PASS WITH REQUIREMENTS

The constitution mandates TDD — tests must be written and reviewed by the user first, and must fail before implementation. For this visual redesign, the following test areas apply:

- **FR-003 test**: A unit test on `PaymentForm` confirming every widget in `Meta.widgets` has `"class": "form-control"` in its attrs.
- **FR-001 test**: An integration test using Django TestClient to GET the payment create page and assert the rendered HTML contains `col-md-6` (not `col-12`).
- **Regression tests**: All existing 292 lines of payment tests must continue to pass after changes.
- **i18n check**: No new user-facing strings are introduced; existing `{% translate %}` usage is preserved.

**Action required in Phase 0**: Determine the exact test approach — widget attrs assertion is straightforward; decide whether to use regex/parsing for HTML assertion or a template-response test.

### Gate 2: User Experience Consistency (i18n)

**Status**: PASS

The existing template already uses `{% translate %}` for all user-facing strings. The redesign does not add or modify any user-facing text. The `PaymentForm` field labels come from the model's `verbose_name` which are already registered in translation files.

### Gate 3: Code Quality (YAGNI, formatting, no dead code)

**Status**: PASS

The redesign reduces a one-off inconsistency (no other form uses `col-12` for all fields). No dead code or complexity added. Complexity Tracking section is not required.

### Gate 4: Performance

**Status**: PASS

No performance impact — template and form class changes only.

### Post-Design Re-check (Phase 1 complete)

- **Gate 1**: Updated PASS — test approach documented in `research.md` and `quickstart.md`. Two new tests defined for FR-001 and FR-003 compliance.
- **Gate 2**: PASS — no new strings.
- **Gate 3**: PASS — no complexity added.
- **Gate 4**: PASS — no performance impact.

## Project Structure

### Documentation (this feature)

```text
specs/023-redesign-payment-form/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       ├── templates/payments/payment_form.html   # EDIT: col-12 → col-md-6
│       ├── forms.py                               # EDIT: add form-control to widget attrs
│       ├── views.py                               # NO CHANGE
│       └── models.py                              # NO CHANGE
└── tests/
    └── test_payments.py                           # ADD: widget attrs & rendered HTML tests
```

**Structure Decision**: Django monolith with apps under `backend/apps/`. The payments app has its own templates, forms, views, and models. Tests are consolidated under `backend/tests/`. This matches the existing project structure — no changes needed.

## Complexity Tracking

*Not required — no complexity violations (Gate 3 PASS).*
