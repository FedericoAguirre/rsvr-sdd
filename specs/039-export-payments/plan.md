# Implementation Plan: Export Payments

**Branch**: `039-export-payments` | **Date**: 2026-07-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/039-export-payments/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Add an "Exportar" button to the existing payments reports page that generates and downloads an .xlsx spreadsheet of payments filtered by the selected date range. Reuses the existing `PaymentReportView` logic and date filter. Streaming/chunked generation for large datasets. Validation error for inverted date ranges. User-friendly error handling with retry on generation failure.

## Technical Context

**Language/Version**: Python 3.13, Django 5.0

**Primary Dependencies**: openpyxl (for .xlsx generation — standard for Django xlsx exports), reportlab (existing, for reference pattern)

**Storage**: PostgreSQL 16

**Testing**: pytest with pytest-django, Django test Client

**Target Platform**: Linux server (Docker), modern web browsers (Bootstrap 5 + htmx)

**Project Type**: Web application (Django)

**Performance Goals**: Export complete in under 5 seconds for 10,000 records

**Constraints**: Files must open in Excel, LibreOffice Calc, Google Sheets. All user-facing strings must be i18n'd to Spanish.

**Scale/Scope**: Single Django view extending existing PaymentReportView. <10k rows typical, streaming for larger datasets.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Results

| # | Principle | Check | Status |
|---|-----------|-------|--------|
| 1 | Code Quality — no dead code, commented code, or unresolved TODOs | Feature adds ~200 lines of new code; no removal expected | PASS ✅ |
| 2 | Testing Standards — TDD mandatory, Red-Green-Refactor, integration tests for contract changes | TDD required: write failing tests first. Integration test: verify exported file matches DB query. | PASS ✅ |
| 3 | User Experience Consistency — i18n NON-NEGOTIABLE, all visible strings translated | Button label "Exportar", alert messages, error messages all need i18n keys + Spanish translations. | PASS ✅ |
| 4 | Performance Requirements — measurable criteria before implementation | SC-001 defines 5s for 10k records. Must benchmark. | PASS ✅ |
| 5 | Dev Environment — uv + Docker, commands run inside container | Implementation runs inside `web` container via `docker compose exec`. | PASS ✅ |
| 6 | Development Workflow — Specify→Plan→Tasks→Implement with review gates | Workflow followed correctly. | PASS ✅ |

**No complexity violations expected** — feature reuses existing views and adds a single new endpoint. YAGNI applies: no separate service layer, no async job queue for v1.

## Project Structure

### Documentation (this feature)

```text
specs/039-export-payments/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       ├── models.py              # No changes needed
│       ├── views.py               # Add PaymentExportView
│       ├── urls.py                # Add export URL
│       └── templates/payments/
│           └── payment_reports.html  # Add "Exportar" button
├── locale/
│   └── es/LC_MESSAGES/
│       └── django.po              # Add i18n entries
└── tests/
    └── test_payments.py           # Add export tests
```

**Structure Decision**: Extend existing Django app (`payments`) with a new view and URL. No new apps, no frontend framework — htmx + Bootstrap 5 as per project conventions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A — no violations.

