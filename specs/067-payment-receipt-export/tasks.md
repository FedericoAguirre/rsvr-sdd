# Tasks: Payment Receipt Export

**Input**: Design documents from `/specs/067-payment-receipt-export/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/receipt-api.md, quickstart.md

**Tests**: Required by the project constitution. Write each story's tests first and verify they fail before implementation.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing runtime and dependency conventions needed by the receipt feature.

- [x] T001 Verify ReportLab 5.0.0, pdfminer.six, pytest-django, and the runtime Unicode font are available in `backend/pyproject.toml`, `backend/uv.lock`, and `backend/Dockerfile`; do not add dependencies unless verification fails.
- [x] T002 [P] Review the existing payment PDF/download conventions in `backend/apps/reservations/views.py`, `backend/tests/test_reservations_list.py`, and `backend/apps/payments/urls.py` and record any required compatibility constraints in `specs/067-payment-receipt-export/research.md`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the shared receipt data boundary used by both formats before story-specific endpoints and UI work.

**Checkpoint**: Shared projection and test scaffolding are ready; user story implementation can proceed.

- [x] T003 Create the shared receipt test module and database fixtures for payments, clients, reservations, class slots, equipment, authenticated operators, and empty payments in `backend/tests/test_payment_receipt.py`.
- [x] T004 [P] Define the localized receipt projection shape, reservation ordering, optional-equipment fallback, and filename sanitization behavior in `backend/apps/payments/receipt.py` according to `specs/067-payment-receipt-export/data-model.md`.
- [x] T005 [P] Add the receipt translation keys and Spanish catalog entries for labels, loading, success, fallback, empty state, and actionable errors in `backend/locale/es/LC_MESSAGES/django.po`.

---

## Phase 3: User Story 1 - Download a payment receipt (Priority: P1) 🎯 MVP

**Goal**: Let an authenticated operator download a localized PDF receipt from the payment detail page with deterministic filenames and complete reservation data.

**Independent Test**: With a payment containing linked reservations, open `/payments/<id>/`, activate `Descargar pago`, and verify the `application/pdf` response, filename, localized header fields, and every reservation row. Repeat with zero reservations and confirm the localized empty-state message.

### Tests for User Story 1

> **TDD**: Write these tests first and confirm they fail before implementation.

- [x] T006 [P] [US1] Add authenticated PDF endpoint contract tests for `200`, `application/pdf`, attachment disposition, payment/client/header values, and linked reservation rows in `backend/tests/test_payment_receipt.py`.
- [x] T007 [P] [US1] Add PDF edge-case tests for zero reservations, missing equipment display, accented/punctuated client names, missing payment reference fallback to payment ID, missing payment `404`, and unauthenticated access in `backend/tests/test_payment_receipt.py`.
- [x] T008 [P] [US1] Add payment-detail template tests for `Descargar pago` placement immediately before `Descargar calendario`, loading-state markup, disabled duplicate activation, and retry/error hooks in `backend/tests/test_payment_detail_template.py`.

### Implementation for User Story 1

- [x] T009 [US1] Implement the receipt projection, localized field formatting, reservation row extraction, and safe filename helper in `backend/apps/payments/receipt.py`.
- [x] T010 [US1] Implement the in-memory ReportLab PDF renderer with a paginated reservation table, Unicode-capable font, localized labels, and localized zero-reservation message in `backend/apps/payments/receipt.py`.
- [x] T011 [US1] Implement the authenticated PDF receipt view with scoped payment retrieval, structured success/failure logging, `application/pdf`, and `Content-Disposition` headers in `backend/apps/payments/views.py`.
- [x] T012 [US1] Register `/api/payments/<int:pk>/receipt/` through `backend/config/urls.py` and `backend/apps/payments/api_urls.py` while preserving the existing `/payments/<int:pk>/calendar/` route behavior.
- [x] T013 [US1] Add the `Descargar pago` action left of `Descargar calendario`, loading spinner/disabled state, actionable failure message, and retry behavior using translated strings in `backend/apps/payments/templates/payments/payment_detail.html`.
- [x] T014 [US1] Run the P1 contract and template tests, extract generated PDF text with pdfminer.six, and verify the independent test criteria in `backend/tests/test_payment_receipt.py` and `backend/tests/test_payment_detail_template.py`.

**Checkpoint**: User Story 1 is independently functional and is the recommended MVP release.

---

## Phase 4: User Story 2 - Share receipt content (Priority: P2)

**Goal**: Let the operator copy the same localized receipt data as Markdown, with a visible manual-copy fallback when clipboard access is unavailable.

**Dependencies**: User Story 2 depends on the shared projection from Phase 2 and the receipt access boundary established in User Story 1.

**Independent Test**: Open `/payments/<id>/`, activate the adjacent Markdown action, paste the result into a plain-text editor, and verify the same localized fields and reservation rows as the PDF. Repeat with clipboard access denied and with zero reservations.

### Tests for User Story 2

> **TDD**: Write these tests first and confirm they fail before implementation.

- [x] T015 [P] [US2] Add Markdown endpoint contract tests for content type, localized header fields, table rows, empty-state message, missing payment, and authentication behavior in `backend/tests/test_payment_receipt.py`.
- [x] T016 [P] [US2] Add payment-detail template tests for the Markdown action, copy-success feedback, clipboard failure fallback, and retry behavior in `backend/tests/test_payment_detail_template.py`.

### Implementation for User Story 2

- [x] T017 [US2] Implement the localized Markdown renderer from the shared receipt projection, preserving the PDF field order and reservation table semantics in `backend/apps/payments/receipt.py`.
- [x] T018 [US2] Implement the authenticated Markdown receipt view and register `/api/payments/<int:pk>/receipt/markdown/` in `backend/apps/payments/views.py` and `backend/apps/payments/api_urls.py`.
- [x] T019 [US2] Add the adjacent Markdown copy action, asynchronous request handling, clipboard API success path, visible text fallback, loading state, and localized status/error messages in `backend/apps/payments/templates/payments/payment_detail.html`.
- [x] T020 [US2] Run the P2 endpoint and template tests and verify Markdown/PDF value parity for populated and empty payments in `backend/tests/test_payment_receipt.py` and `backend/tests/test_payment_detail_template.py`.

**Checkpoint**: User Stories 1 and 2 are independently testable and preserve the same receipt data contract.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate quality, localization, performance, security, and documentation across both stories.

- [x] T021 [P] Compile and verify the updated Spanish translations and scan all receipt UI/template strings for untranslated literals in `backend/locale/es/LC_MESSAGES/django.po` and `backend/apps/payments/templates/payments/payment_detail.html`.
- [x] T022 [P] Add representative 50-reservation timing coverage or a documented profiling run for the 10-second target in `backend/tests/test_payment_receipt.py` and record the result in `specs/067-payment-receipt-export/quickstart.md`.
- [x] T023 [P] Review receipt logs and error responses for payment-ID-only structured context, no receipt contents or personal data, and no partial PDF response in `backend/apps/payments/views.py` and `backend/apps/payments/receipt.py`.
- [x] T024 Run the complete documented validation flow from `specs/067-payment-receipt-export/quickstart.md` and the full backend project test suite from `backend/`; record any failures before implementation completion in `specs/067-payment-receipt-export/quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; T001 and T002 can run in parallel.
- **Foundational (Phase 2)**: Depends on Setup; T003, T004, and T005 can run in parallel, but story implementation starts only after the shared projection contract is agreed.
- **User Story 1 (Phase 3)**: Depends on Foundational; tests T006-T008 must fail before implementation T009-T013.
- **User Story 2 (Phase 4)**: Depends on Foundational and the access/projection boundary from User Story 1; tests T015-T016 must fail before implementation T017-T019.
- **Polish (Phase 5)**: Depends on both desired user stories; T021-T023 can run in parallel before T024.

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on Foundational and is the MVP.
- **User Story 2 (P2)**: Reuses the projection and protected access boundary from User Story 1; it does not require a new data model or migration.

### Parallel Opportunities

- **Setup**: T001 and T002 can run concurrently because they inspect different files.
- **Foundational**: T003, T004, and T005 can run concurrently after agreeing on the projection fields.
- **US1 tests**: T006, T007, and T008 can run concurrently because they cover separate test concerns/files.
- **US2 tests**: T015 and T016 can run concurrently.
- **Polish**: T021, T022, and T023 can run concurrently after implementation.

## Parallel Example: User Story 1

```text
Task T006: PDF endpoint contract tests in backend/tests/test_payment_receipt.py
Task T007: PDF edge-case tests in backend/tests/test_payment_receipt.py
Task T008: Payment detail template tests in backend/tests/test_payment_detail_template.py
```

## Parallel Example: User Story 2

```text
Task T015: Markdown endpoint contract tests in backend/tests/test_payment_receipt.py
Task T016: Markdown UI/fallback tests in backend/tests/test_payment_detail_template.py
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Write and review failing US1 tests before implementation.
3. Implement the shared projection, PDF renderer, protected endpoint, route, and detail-page action.
4. Run the independent US1 validation and stop for review/demo.

### Incremental Delivery

1. Deliver US1 as the formal PDF receipt MVP.
2. Add US2 Markdown sharing without changing receipt data semantics.
3. Complete cross-cutting localization, performance, security, and quickstart validation.

### Environment Reference

- **Run feature tests** from `backend/`: `uv run pytest tests/test_payment_receipt.py tests/test_payment_detail_template.py`
- **Run full tests** from `backend/`: `uv run pytest`
- **Start PostgreSQL**: `make db-up`
- **Validate Docker stack before release**: `make docker-build && make docker-up`

## Notes

- Every task follows the required checklist format with a sequential ID, optional `[P]`, required story labels in story phases, and concrete file paths.
- No migration task is included because the data model is derived from existing tables.
- Do not add a task queue in this release; revisit only if measured receipt latency or volume exceeds the documented target.
