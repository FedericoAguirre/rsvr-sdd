# Implementation Plan: Price Format Display

**Branch**: `063-price-format` | **Date**: 2026-08-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/063-price-format/spec.md`

## Summary

Format class price amounts on the class prices page as `$N,NNN.NN` (dollar sign, comma thousand separators, dot decimal, two decimal places). Currently prices are rendered as raw `Decimal` values (`100.00`) without any formatting. The existing `currency` template filter in `payment_extras` already produces this exact format and will be reused. No data model or schema changes required — pure presentation-layer change.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Django 5.0

**Storage**: PostgreSQL (no schema changes — existing `ClassPrice.price` DecimalField)

**Testing**: pytest (Django test framework)

**Target Platform**: Linux server (Docker), local macOS dev

**Project Type**: Web application (Django monolith)

**Performance Goals**: Negligible impact — string formatting on Decimal values during template rendering

**Constraints**: N/A (presentation-only change)

**Scale/Scope**: Single template (`class_prices.html`), 2 locations within that template (current prices alert + history table). One template filter import.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | PASS | Template-only change, no dead code, no complexity addition |
| II. Testing Standards | PASS | Integration tests will verify formatted output in rendered HTML. No new library contracts. |
| III. UX Consistency / i18n | PASS | Format matches existing `payment_extras.currency` filter. No new user-visible strings introduced — only numeric formatting. `$` symbol is already consistent across payment templates. |
| IV. Performance | PASS | `float(value):,.2f` formatting is O(1) per value. No measurable impact on render time. |
| V. External Documentation | PASS | Django 5.0 template tags/filters docs to be consulted via Context7 before implementation. |

**Gate Result**: All principles pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/063-price-format/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   ├── classes/
│   │   └── templates/classes/
│   │       └── class_prices.html          # PRIMARY: apply currency filter to {{ price.price }}
│   └── payments/
│       └── templatetags/
│           └── payment_extras.py          # Existing currency filter — reuse or move
└── tests/
    └── classes/
        └── test_templates.py              # NEW: render tests for formatted price output
```

**Structure Decision**: Single Django app change. The `currency` filter in `payment_extras.py` is the existing formatting utility. Options are: (A) load `payment_extras` in the classes template, or (B) extract the `currency` filter to a shared `core/templatetags/` module. Research phase will determine best approach considering app coupling.

## Complexity Tracking

> No constitutional violations — this section is empty.
