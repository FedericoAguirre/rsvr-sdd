# Implementation Plan: Batch Reservations from Payment

**Branch**: `048-batch-reservations-payment` | **Date**: 2026-07-20 | **Spec**: `specs/048-batch-reservations-payment/spec.md`

**Input**: Feature specification from `specs/048-batch-reservations-payment/spec.md`

## Summary

After saving a payment, a modal lets the operator batch-create N reservations (N = block class count, max 20) by selecting equipment, a class slot, and exactly N DOW-matching dates within a 4-week window starting from the next Monday. Each reservation links to the payment via PaymentReservation.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.0.x

**Storage**: PostgreSQL 16

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker)

**Project Type**: Web application (Django templates + Bootstrap 5)

**Performance Goals**: Batch creation completes within 5 seconds (SC-002); modal appears without noticeable delay after payment save

**Constraints**: <200ms standard page loads; modal respects existing unique constraints (equipment + class_slot + date); partial failure on conflicts

**Scale/Scope**: Small business (single gym); <50 concurrent operators; single payment creates ≤20 reservations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No constitution file found — gates skipped.

## Project Structure

### Documentation (this feature)

```text
specs/048-batch-reservations-payment/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   ├── payments/
│   │   ├── models.py          # Payment, PaymentReservation (existing)
│   │   ├── views.py           # New: batch_create view + modal endpoint
│   │   ├── forms.py           # New: BatchReservationForm
│   │   ├── urls.py            # New: batch endpoint routes
│   │   └── templates/
│   │       └── payments/
│   │           ├── payment_form.html        # Modified: add modal trigger
│   │           ├── payment_detail.html       # Modified: show associated reservations
│   │           └── _batch_modal.html         # New: batch reservation modal
│   └── reservations/
│       └── models.py          # Reservation (existing, no changes)
├── tests/
│   ├── test_payments.py       # New: batch creation tests
│   └── test_payments_batch.py # New: batch-specific edge case tests
└── locale/
    └── es/
        └── django.po          # Updated: new Spanish translations
```

**Structure Decision**: Django app structure — changes isolated to `payments` app with a new batch modal template, form, and view. The `reservations` model is reused (unchanged). Tests added to `tests/test_payments.py`.

## Complexity Tracking

No constitution violations — complexity tracking skipped.

## Phase 0: Research

All technical context is known from the existing project. No NEEDS CLARIFICATION markers remain.

## Phase 1: Design

See:
- `data-model.md` — entity definitions and relationships
- `contracts/` — batch reservation contracts/APIs
- `quickstart.md` — how to run and test this feature
