# Implementation Plan: Switch Date and Class Block Columns in Payments History

**Branch**: `043-switch-date-class-columns` | **Date**: 2026-07-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/043-switch-date-class-columns/spec.md`

## Summary

Reorder the reservation history table columns on the client detail page (`clients/{id}/`) from current order (Date, Class, Equipment) to desired order (Class, Date, Equipment). This is a purely presentational change — only the `<th>` and `<td>` element order in the HTML template needs to change.

## Technical Context

**Language/Version**: Python 3.13 (Django 5.0)

**Primary Dependencies**: Django templates, Django i18n (`{% translate %}`)

**Storage**: PostgreSQL 16 (no schema changes)

**Testing**: pytest (functional test on rendered HTML)

**Target Platform**: Linux (Docker), macOS dev

**Project Type**: Web application (Django + Bootstrap 5)

**Performance Goals**: N/A — cosmetic template-only change, zero performance impact

**Constraints**: Column header labels and data must remain unchanged; only visual order changes

**Scale/Scope**: Single template file change

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **TDD** (Testing Standards §II) | ✅ PASS | Tests can verify column order via HTML content inspection |
| **i18n** (UX Consistency §III) | ✅ PASS | All three column labels are already translated — no i18n work needed |
| **Code Quality** (§I) | ✅ PASS | Minimal change, no dead code, no complexity added |
| **Performance** (§IV) | ✅ PASS | Not applicable |
| **Complexity** (YAGNI) | ✅ PASS | Single template reorder — no complexity concerns |

## Project Structure

### Documentation (this feature)

```text
specs/043-switch-date-class-columns/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A — no data changes)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A — no external interfaces)
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── clients/
│       └── templates/
│           └── clients/
│               └── client_detail.html   # ← ONE FILE TO CHANGE
└── tests/
    └── test_client_detail.py             # ← NEW test file
```

**Structure Decision**: Standard Django app layout. Single template modification in `clients/client_detail.html`. New test module `test_client_detail.py`.

## Complexity Tracking

> N/A — no constitutional violations to justify.
