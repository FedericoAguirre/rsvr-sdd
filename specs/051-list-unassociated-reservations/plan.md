# Implementation Plan: List Unassociated Reservations on Payments Page

**Branch**: `051-list-unassociated-reservations` | **Date**: 2026-07-24 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/051-list-unassociated-reservations/spec.md`

## Summary

Add a filtered list of unassociated reservations to the client payments page (`payments/client/<int:client_id>/`) so staff users can see which of a client's reservations still need payment association. The view will query reservations belonging to the client that have no `PaymentReservation` link and render them alongside the existing payment history.

## Technical Context

**Language/Version**: Python 3.12 (Django 5.0)

**Primary Dependencies**: Django 5.0, pytest, Bootstrap 5.3, HTMX 2.x

**Storage**: PostgreSQL (existing)

**Testing**: pytest via `docker compose exec web uv run pytest`

**Target Platform**: Linux server (Docker Compose)

**Project Type**: Web application (Django)

**Performance Goals**: Page load time should not increase compared to the existing client payment page. The reservation query adds a single indexed query (filter by `client_id`, exclude associated via `payment_links`).

**Constraints**:
- Must reuse existing `Reservation` and `PaymentReservation` models (no schema changes)
- Must integrate into the existing `payments/client/<int:client_id>/` page (`ClientPaymentHistoryView`)
- Existing payment history list must remain unchanged
- All new user-visible strings must be internationalized (i18n)
- Reservation filter: `client_id = URL param`, exclude where `PaymentReservation` exists

**Scale/Scope**: Small feature — extend existing view + template, one new queryset filter, one new section in template, empty-state handling.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **I. Code Quality** | ✅ PASS | No dead code or duplication; follows existing `ClientPaymentHistoryView` pattern |
| **II. Testing Standards** | ✅ PASS | Red-Green-Refactor: tests for queryset filter, empty state, and page rendering |
| **III. UX Consistency (i18n)** | ✅ PASS | All new strings (section heading, empty state) must use `{% translate %}` / `gettext` |
| **IV. Performance** | ✅ PASS | Single indexed query via `client_id` FK; no N+1 risk with `select_related` |
| **V. External Docs** | ✅ PASS | No new library dependencies; existing Django ORM patterns only |

## Project Structure

### Documentation (this feature)

```text
specs/051-list-unassociated-reservations/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 — research artifacts
├── data-model.md        # Phase 1 — entity definitions
├── quickstart.md        # Phase 1 — development quickstart
├── contracts/           # Phase 1 — interface contracts (if applicable)
└── tasks.md             # Phase 2 — implementation tasks (generated later)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       ├── views.py                    # Extend ClientPaymentHistoryView to pass unassociated reservations
│       └── templates/
│           └── payments/
│               └── payment_list.html   # Add unassociated reservations section
└── tests/
    └── test_payments_unassociated_reservations.py  # NEW: tests for this feature
```

**Structure Decision**: Django web application — single backend project with app-based separation. Feature lives entirely within the existing `payments` app; no new apps or utilities needed.

## Complexity Tracking

> No constitution violations to justify. Feature is small, single-view extension with no new models.
