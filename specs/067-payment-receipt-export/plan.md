# Implementation Plan: Payment Receipt Export

**Branch**: `067-payment-receipt-export` | **Date**: 2026-08-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/067-payment-receipt-export/spec.md`

## Summary

Add receipt actions to the payment detail page. A protected backend receipt boundary will aggregate the selected payment, client, and linked reservations once, render localized Markdown or an in-memory PDF, and return download-safe headers. The PDF uses the existing ReportLab dependency and the Markdown action uses the same normalized receipt data, avoiding duplicated business rules.

## Technical Context

<!--
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Django 5.0.x, ReportLab 5.0.0 (already locked), Bootstrap 5.3 via existing templates, pdfminer.six for PDF-content tests

**Storage**: Existing PostgreSQL Payment, Client, PaymentReservation, Reservation, ClassSlot, and Equipment records; no new tables or migrations

**Testing**: pytest 9.1.x with pytest-django 4.12.x; PDF text assertions with existing pdfminer.six dependency; authenticated Django test client

**Target Platform**: POSIX-hosted Django web application, desktop and mobile browsers

**Project Type**: Server-rendered Django web application with protected HTTP download endpoints

**Performance Goals**: At least 95% of receipts with up to 50 reservations complete within 10 seconds; normal requests should issue one bounded reservation query with related objects selected

**Constraints**: Generate in memory; return `application/pdf` with attachment disposition; preserve active-language translations and Latin-script accents; use a Unicode-capable font available in the runtime image; avoid unsafe filename characters; log generation failures with structured context; no asynchronous queue in this release

**Scale/Scope**: One payment receipt at a time, expected up to 50 associated reservations in the primary performance target; larger sets must paginate in the PDF and retain all rows

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality**: PASS. Keep receipt logic cohesive, formatted with Ruff, and free of dead code or unresolved TODOs.
- **Testing**: PASS with required TDD sequencing. Add failing view, rendering, filename, empty-state, permission, and template tests before implementation; include integration coverage for the HTTP/PDF boundary.
- **UX and i18n**: PASS with conditions. All new button, loading, error, fallback, receipt, and empty-state strings use Django translations and active-language output. Update user-facing documentation in the quickstart or project docs as appropriate.
- **Performance and observability**: PASS with conditions. Record generation success/failure and payment identifier without receipt contents or personal data; verify the 10-second target for the representative reservation volume and document the measurement in implementation validation.
- **Dependency integrity**: PASS. ReportLab, Django, and pytest-django usage is based on current Context7 documentation; no new dependency is required.
- **Security**: PASS. Reuse authenticated payment-detail access, scope every query by the requested payment, and do not expose receipts to unauthenticated users.

## Project Structure

### Documentation (this feature)

```text
specs/067-payment-receipt-export/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── apps/payments/
│   ├── models.py                         # Existing Payment and PaymentReservation models
│   ├── receipt.py                         # Normalized receipt data, Markdown, PDF, filename helpers
│   ├── api_urls.py                        # Protected receipt API routes
│   ├── urls.py                            # Existing payment routes plus receipt routes
│   ├── views.py                           # Protected receipt endpoint(s)
│   └── templates/payments/payment_detail.html # Receipt actions and loading/fallback UI
├── config/urls.py                         # `/api/payments/<id>/receipt/` route include
├── locale/es/LC_MESSAGES/django.po        # New translated UI and receipt strings
├── tests/
│   ├── test_payment_receipt.py            # Contract and PDF/Markdown integration tests
│   └── test_payment_detail_template.py    # Receipt action/template assertions
└── pyproject.toml                         # Existing dependencies; no new package expected
```

**Structure Decision**: Extend the existing `backend/apps/payments` module. Keep receipt formatting in a focused module so the PDF and Markdown representations share one data projection, while views remain responsible for authentication and HTTP responses. Add API routing at the project URL root because the specified receipt contract uses `/api/payments/{id}/receipt` rather than the existing HTML `/payments/` namespace.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The design stays within the existing payments app and uses an already-declared PDF dependency. |
