# Implementation Plan: Remove Custom Range

**Branch**: `033-remove-custom-range` | **Date**: 2026-07-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/033-remove-custom-range/spec.md`

## Summary

Remove the "Custom Range" (`range`) option from the "Group by" dropdown on the Reports > Payments page and delete all associated backend handling code. The `range` grouping is functionally identical to `day` grouping, so no functionality is lost. Graceful fallback to month grouping for any lingering `?grouping=range` requests.

## Technical Context

**Language/Version**: Python 3.12 (Docker), JavaScript (ES6+ in browser)

**Primary Dependencies**: Django 5.x, Chart.js 4

**Storage**: PostgreSQL — no schema changes required

**Testing**: pytest via `docker compose exec web uv run manage.py test`

**Target Platform**: Linux server (Docker), modern browsers (Chrome, Firefox, Safari)

**Project Type**: Web application — Django monolith with Bootstrap 5.3.3

**Performance Goals**: No performance impact — code removal only

**Constraints**: Date range inputs must remain functional for Day/Week/Month groupings. Zero regressions on remaining groupings.

**Scale/Scope**: Two files changed: view (`payments/views.py`) and template (`payment_reports.html`). One test updated.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| i18n (NON-NEGOTIABLE) | ✅ PASS | No new strings; remove existing "Custom Range" key from django.po |
| TDD | ✅ PASS | Update existing `test_reports_day_grouping_with_date_range` — remove range-specific test |
| Code Quality | ✅ PASS | Dead code removal — clean with ruff |
| YAGNI | ✅ PASS | Removal of unused option — simplifies UI |
| Complexity Tracking | ✅ N/A | No complexity additions |

## Project Structure

### Documentation (this feature)

```text
specs/033-remove-custom-range/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (changed files)

```text
backend/apps/payments/views.py                           # Remove `range` case from PaymentReportView
backend/apps/payments/templates/payments/payment_reports.html  # Remove "Custom Range" dropdown option
backend/tests/test_payments.py                           # Update/remove range test case
backend/locale/es/LC_MESSAGES/django.po                  # Remove "Custom Range" i18n entry
```

**Structure Decision**: Django monolith — changes across view, template, test, and locale files.

## Complexity Tracking

> No complexity additions. This is a removal-only change.
