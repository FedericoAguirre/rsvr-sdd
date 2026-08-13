# Implementation Plan: Payment Receipt Identifier Integration

**Branch**: `068-update-payment-identifier` | **Date**: 2026-08-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/068-update-payment-identifier/spec.md`

## Summary

Update the existing payment receipt projection so the public `payment_identifier` replaces the legacy `payment_reference`/`reference` value in PDF content, Markdown content, and PDF download filenames. Preserve the existing authenticated endpoints, payment detail actions, calendar download, and copy-only Markdown behavior. Add focused regression coverage for rendered identifier content, sanitized filenames, and unchanged calendar/UI behavior.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Existing Django receipt views and translations, ReportLab PDF rendering, pytest/pytest-django, pdfminer.six PDF assertions; no new dependency

**Storage**: Existing PostgreSQL `Payment`, `Client`, `PaymentReservation`, `Reservation`, `ClassSlot`, and `Equipment` records; no schema or migration changes

**Testing**: pytest 9.1.x with pytest-django 4.12.x; PDF text assertions through existing pdfminer.six; source-level payment-detail regression checks; existing calendar endpoint tests

**Target Platform**: POSIX-hosted Django web application, desktop and mobile browsers

**Project Type**: Server-rendered Django web application with authenticated HTTP receipt and calendar download endpoints

**Performance Goals**: Preserve the existing receipt-generation target: at least 95% of receipts with up to 50 reservations complete within 10 seconds; the identifier substitution must add no additional database query or materialization pass

**Constraints**: Keep receipt data centralized in `build_receipt()`; use the existing sanitized filename helper; preserve active-language output and accented receipt content; keep the PDF as an attachment; do not introduce a Markdown file download because the current Markdown action copies content to the clipboard; retain authentication and existing payment selection boundaries

**Scale/Scope**: One selected payment per request, with the existing expected volume of up to 50 associated reservations; changes are limited to receipt projection/rendering, translations, tests, and supporting validation documentation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality**: PASS. The change reuses the existing receipt projection and filename helper, avoids new abstractions, and requires Ruff formatting/linting with no dead code or unresolved TODOs.
- **Testing**: PASS with conditions. Tests must be updated or added before implementation and fail against the current reference-based behavior. Coverage must include PDF content, Markdown content, sanitized filename output, empty receipts, authentication, and calendar regression; the existing 50-reservation integration/performance test remains required.
- **UX and i18n**: PASS with conditions. Add a translated receipt label for the public payment identifier, preserve active-language rendering, and keep the existing payment detail actions and error/loading behavior unchanged. The quickstart documents user-visible validation.
- **Performance and observability**: PASS with conditions. Keep the current single receipt-data projection and reservation query, preserve the 10-second representative-volume test, and continue structured generation success/failure logs without receipt contents or personal data.
- **Dependency integrity**: PASS. No dependency is added or upgraded. Django response/authentication conventions were checked against current authoritative documentation; existing ReportLab and pdfminer.six usage remains unchanged.
- **Security**: PASS. Keep the existing authenticated views, scope receipt data to the requested payment, and continue sanitizing client and identifier filename components so path separators and control characters cannot become download-path input.

## Project Structure

### Documentation (this feature)

```text
specs/068-update-payment-identifier/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 decisions and findings
├── data-model.md        # Receipt projection and existing entity mapping
├── quickstart.md        # End-to-end validation guide
├── contracts/
│   └── receipt-downloads.md # Existing PDF and Markdown HTTP/UI contracts
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
backend/
├── apps/payments/
│   ├── receipt.py                         # Public identifier in projection, Markdown, PDF, and filename
│   ├── views.py                           # Existing authenticated receipt endpoints; behavior preserved
│   ├── templates/payments/payment_detail.html # Existing receipt/calendar controls; regression-only verification
│   └── api_urls.py                        # Existing receipt routes; unchanged
├── locale/es/LC_MESSAGES/django.po       # Spanish public-identifier receipt label
└── tests/
    ├── test_payment_receipt.py            # PDF/Markdown identifier and filename coverage
    ├── test_payment_detail_template.py   # Receipt/calendar UI regression coverage
    └── test_payments_calendar.py          # Existing calendar download regression coverage
```

**Structure Decision**: Extend the existing `apps.payments.receipt` projection rather than introducing a new service or model. Keep HTTP routing and authentication unchanged. Use the existing translation catalog and receipt integration tests, adding only the cases needed to prove the identifier replacement and preserve adjacent behavior.

## Complexity Tracking

No violations. The design changes one existing receipt value and its consumers; no new project, dependency, persistence model, endpoint, or client workflow is required.
