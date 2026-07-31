# Implementation Plan: Compact Payment Form Layout for Single-Screen View

**Branch**: `055-compact-payment-form` | **Date**: 2026-07-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/055-compact-payment-form/spec.md`

## Summary

Modify the payment creation/edit template (`payment_form.html`) and its embedded CSS to reduce form height by ~25% (from ~800px to ~550–600px) so all fields fit in a 1080p viewport without scrolling. Changes are CSS-only: reduced spacing (`mb-4`→`mb-2`, `mb-3`→`mb-2`), smaller title (`h2`→`h4`), collapsed help text by default, and optimized column layouts (Documentation section from 2-col+full-width to 3-col; Date+Notes from stacked to side-by-side).

## Technical Context

**Language/Version**: Python 3.12 (Django 5.0)

**Primary Dependencies**: Bootstrap 5.3 (embedded via CDN or project static), Django i18n framework

**Storage**: None — no data model changes

**Testing**: pytest via `uv run pytest apps/payments/tests/`

**Target Platform**: Desktop web (1080p+ primary), tablet/mobile responsive (maintained, not redesigned)

**Project Type**: Django web application (backend-rendered templates with Bootstrap 5.3 frontend)

**Performance Goals**: N/A — no backend changes; template rendering time unaffected

**Constraints**: Form must fit in 600px or less vertical space including all fields and buttons on 1080p displays

**Scale/Scope**: Single template file (`payment_form.html`) plus embedded CSS and optional JS for help text toggle

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Notes |
|-----------|-------|-------|
| I. Code Quality | PASS | No dead code, YAGNI applied (CSS-only, no backend changes) |
| II. Testing Standards (NON-NEGOTIABLE) | PASS | Existing tests cover form rendering, validation, submission; no new tests needed for CSS-only changes |
| III. UX Consistency / i18n (NON-NEGOTIABLE) | PASS | All existing i18n strings preserved; no new user-visible strings introduced |
| IV. Performance Requirements | PASS | No backend changes; no performance impact |
| V. External Documentation & Dependency Integrity | PASS | Bootstrap 5.3 docs queried via Context7 for form utilities, spacing, and responsive patterns |

**No violations found. Complexity Tracking section not required.**

## Project Structure

### Documentation (this feature)

```text
specs/055-compact-payment-form/
├── plan.md              # This file
├── research.md          # Phase 0 — Bootstrap 5.3 form utilities, layout research
├── data-model.md        # Phase 1 — template structure and column layout
├── quickstart.md        # Phase 1 — validation scenarios
├── contracts/
│   └── README.md        # Phase 1 — UI contract invariants
├── spec.md              # Feature specification
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code (repository root)

```text
backend/
└── apps/
    └── payments/
        └── templates/
            └── payments/
                └── payment_form.html   # [MODIFY] Compact layout, CSS, and JS
```

**Structure Decision**: Web application (Django monolith with Bootstrap frontend). Only the single template file is modified.

## Complexity Tracking

> Not required — no constitution violations.
