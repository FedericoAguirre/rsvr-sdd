# Implementation Plan: Payments Labels Change

**Branch**: `032-payments-labels-change` | **Date**: 2026-07-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-payments-labels-change/spec.md`

## Summary

Update labels, placeholders, and button styles on the payments listing page to match the clients/search page wording and conventions. Changes are purely presentational — no backend logic, data model, or URL changes required.

## Technical Context

**Language/Version**: Python 3.12 (Django 5.x), HTML/Django Templates (Bootstrap 5.3.3, HTMX 2.0.4)

**Primary Dependencies**: Django, django-bootstrap (via CDN Bootstrap 5.3.3), HTMX 2.0.4

**Storage**: N/A — no schema or model changes

**Testing**: Django Test Client (pytest), existing integration tests in `backend/tests/test_payments*.py`

**Target Platform**: Web (Docker-based, Linux container)

**Project Type**: Web application (Django monolith with HTMX frontend)

**Performance Goals**: N/A — purely presentational changes

**Constraints**: Every user-visible string MUST use i18n (constitutional requirement, zero exceptions). All label changes must reuse existing translation keys.

**Scale/Scope**: Single template file (`payment_list.html`) + i18n `.po`/`.mo` updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **G1: i18n Compliance** | PASS (conditional) | All new/changed strings exist in `django.po` as translations from `clients/search`. No new translation keys needed. Verify after implementation. |
| **G2: Testing Standards (TDD)** | PASS (conditional) | Existing integration tests exist for payments. Label/style changes require updating existing tests. Tests must verify the new labels and class names. |
| **G3: Code Quality** | PASS | Changes are limited to one template file and i18n files. No complexity concern. |
| **G4: Performance** | PASS | No performance impact from presentational changes. |

## Project Structure

### Documentation (this feature)

```text
specs/001-payments-labels-change/
├── plan.md              # This file
├── research.md          # Phase 0 — research findings
├── data-model.md        # Phase 1 — no model changes (N/A)
├── quickstart.md        # Phase 1 — implementation steps
└── contracts/           # Phase 1 — no interface contracts (N/A)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       └── templates/
│           └── payments/
│               └── payment_list.html        # ONLY file requiring code changes
├── locale/
│   └── es/
│       └── LC_MESSAGES/
│           ├── django.po                    # i18n source — add/remove entries
│           └── django.mo                    # i18n compiled — regenerate
└── tests/
    └── test_payments_search.py             # Update tests for new labels/classes
```

**Structure Decision**: Django monolith — single project with app-based organization. Changes confined to payments app template and i18n files.

## Complexity Tracking

No violations — this feature is a straightforward presentational change. Complexity Tracking section is not needed.
