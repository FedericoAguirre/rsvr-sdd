# Implementation Plan: Order Reservations by Date in Payment Detail

**Branch**: `042-order-reservations-date` | **Date**: 2026-07-14 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/042-order-reservations-date/spec.md`

## Summary

Add explicit ordering by reservation date (descending) and class slot time (descending) to the payment detail page's reservation list. Currently the queryset in `PaymentDetailView.get_context_data()` calls `.all()` with no `.order_by()`, falling back to PK order. The fix adds `.order_by("-reservation__date", "-reservation__class_slot__time")` to match the pattern already used in `PaymentAssociateView`.

## Technical Context

**Language/Version**: Python 3.13, Django 5.0

**Primary Dependencies**: Django ORM, PostgreSQL 16

**Storage**: PostgreSQL 16

**Testing**: pytest 8.x, pytest-django, Django TestCase

**Target Platform**: Linux server (Docker container)

**Project Type**: Web application (Django + Bootstrap 5)

**Performance Goals**: N/A — simple query sort change, no measurable performance impact

**Constraints**: No new queries or N+1 patterns; must reuse the existing `select_related` chain

**Scale/Scope**: Single view change in `PaymentDetailView`; ~1-3 lines of code; scope bounded to the payment detail page only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **TDD** — Tests must be written and failing before implementation | ⚠️ PENDING | Need to add ordering assertions to existing `test_payment_detail_shows_associated_reservations` test (or create new test) — must fail first |
| **i18n** — No hardcoded user-visible strings | ✅ PASS | No new strings introduced |
| **Code Quality** — YAGNI, no dead code | ✅ PASS | ~3 line change, no complexity added |
| **Performance** — Measurable criteria defined | ✅ PASS | No measurable performance concern for a sort change on an already-loaded queryset |
| **No commented-out code or TODOs** | ✅ PASS | Will ensure clean commit |

**Phase 1 re-check**: No design complexity introduced — this is a straight ordering change. Re-check is satisfied automatically.

## Project Structure

### Documentation (this feature)

```text
specs/042-order-reservations-date/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       └── views.py           # <-- CHANGE: add .order_by() to reservation queryset
└── tests/
    └── test_payments.py        # <-- CHANGE: add ordering tests
```

**Structure Decision**: Standard Django project layout. Only two files change: the view (add `.order_by()`) and the test file (add ordering assertions).

## Complexity Tracking

> No Constitution Check violations — Complexity Tracking is empty.
