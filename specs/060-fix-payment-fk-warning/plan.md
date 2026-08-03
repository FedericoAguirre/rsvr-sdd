# Implementation Plan: Fix PaymentReservation ForeignKey Warning

**Branch**: `060-fix-payment-fk-warning` | **Date**: 2026-08-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/060-fix-payment-fk-warning/spec.md`

## Summary

Replace `models.ForeignKey(unique=True)` with `models.OneToOneField` on `PaymentReservation.reservation` to eliminate the Django `fields.W342` system check warning. The semantic meaning is unchanged — each reservation has at most one payment link — but the field type now matches the intent.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Django 5.0.x, psycopg2-binary

**Storage**: PostgreSQL 16

**Testing**: pytest 9.1.x with pytest-django

**Target Platform**: Linux server (Docker)

**Project Type**: Web application (Django backend)

**Performance Goals**: N/A (field-type substitution, no performance impact)

**Constraints**: Zero-downtime migration; existing data must be preserved

**Scale/Scope**: Single field change on one model; ~4 references in views; 1 migration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No constitution file exists at `.specify/memory/constitution.md`. Proceeding without constitution gates.

## Project Structure

### Documentation (this feature)

```text
specs/060-fix-payment-fk-warning/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       ├── models.py            # PaymentReservation.reservation field change
│       ├── views.py             # No changes (queryset filters work identically)
│       └── migrations/          # Auto-generated migration
└── tests/                       # Existing test suite for regression
```

**Structure Decision**: Single Django backend application. The change is localized to `backend/apps/payments/models.py` with an auto-generated migration.

## Complexity Tracking

No violations. No complexity added.
