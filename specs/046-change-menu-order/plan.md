# Implementation Plan: Change navigation bar menu order

**Branch**: `046-change-menu-order` | **Date**: 2026-07-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/046-change-menu-order/spec.md`

## Summary

Reorder the navigation bar menu items in `backend/templates/base.html` from their current order (Reservations, Clients, Equipment, Schedule, Payments, Reports, Admin, Logout) to the specified workflow order: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión. All items already use `{% translate %}` for i18n — no string changes needed.

## Technical Context

**Language/Version**: Python 3.12+, Django

**Primary Dependencies**: Django, Bootstrap 5, django-htmx, i18n (django-modeltranslation)

**Storage**: N/A (no data changes)

**Testing**: pytest (pytest-django)

**Target Platform**: Linux (Docker), web browser

**Project Type**: Web application (Django)

**Performance Goals**: N/A — static template change, no runtime impact

**Constraints**: Zero functional regression — all links, dropdowns, active states, conditional visibility, and form-based logout must work identically

**Scale/Scope**: Single file change — `backend/templates/base.html`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| I. Code Quality | ✅ PASS | Simple reorder, linter will catch any formatting issues |
| II. Testing Standards (NON-NEGOTIABLE) | ⚠️ TDD REQUIRED | Existing `test_navbar_brand_and_nav_links_spanish` in `test_i18n.py` checks Spanish labels but not order. A new test MUST be written first (before reordering) that verifies the specific menu item order in the rendered HTML. The existing test will continue to pass. |
| III. UX Consistency / i18n (NON-NEGOTIABLE) | ✅ PASS | All nav labels already use `{% translate %}`. No new strings introduced. |
| IV. Performance | ✅ PASS | No performance impact |
| Dev Workflow | ✅ PASS | Single-file change on feature branch |

**Gate Decision**: PROCEED — TDD test must be written before implementation per Constitution §II.

## Project Structure

### Documentation (this feature)

```text
specs/046-change-menu-order/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (no new entities)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── templates/
│   └── base.html        # Navbar definition — single file to modify
└── tests/
    └── test_i18n.py     # Existing test (will continue to pass)
                         # + new test for menu item order (TDD)
```

## Phase 0: Research

All technical context is known — no NEEDS CLARIFICATION markers. The only research task is confirming the current nav structure (already verified by reading `base.html` lines 17-40).

## Phase 1: Design & Contracts

### Data Model

No new entities. This is a presentation-order change only.

### Contracts

None — purely internal template change.

### Quickstart

1. Write a TDD test that renders any page and asserts the nav `<li>` elements appear in the correct left-to-right order
2. Confirm test fails (red)
3. Reorder `<li>` elements in `backend/templates/base.html` (green)
4. Run full test suite to confirm no regressions

## Complexity Tracking

No complexity additions — single `<li>` reorder, no new patterns or dependencies.
