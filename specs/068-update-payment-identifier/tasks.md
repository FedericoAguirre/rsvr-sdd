# Tasks: Payment Receipt Identifier Integration

**Input**: Design documents from `/specs/068-update-payment-identifier/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Required by the project constitution. Each story's tests must be written and confirmed failing before its implementation task.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the existing baseline and confirm the change remains representation-only.

- [X] T001 Run the baseline receipt, payment-detail template, and calendar tests from `backend/tests/test_payment_receipt.py`, `backend/tests/test_payment_detail_template.py`, and `backend/tests/test_payments_calendar.py` using `uv run pytest` and record the current reference-based expectations before implementation.
- [X] T002 [P] Confirm the implementation remains migration-free by reviewing `backend/apps/payments/models.py`, `backend/apps/payments/api_urls.py`, and `backend/pyproject.toml`; do not add model fields, routes, or dependencies.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Prepare shared translated output required by all receipt representations.

- [X] T003 [P] Verify the existing translated public payment-identifier receipt label in `backend/locale/es/LC_MESSAGES/django.po`, preserving the project’s existing i18n conventions and active-language behavior.

**Checkpoint**: Existing routes, authentication, data relationships, dependencies, and shared translation prerequisites are confirmed before story implementation.

---

## Phase 3: User Story 1 - Identify the Payment Receipt (Priority: P1) 🎯 MVP

**Goal**: Show `payment_identifier` clearly in the PDF receipt and remove the legacy reference from the visual receipt identifier.

**Independent Test**: Generate an authenticated PDF for a payment with different `payment_identifier` and `reference` values, extract the PDF text, and verify the identifier is present while the legacy reference is absent from the reference field.

### Tests for User Story 1

> Write these tests first and confirm they fail against the current reference-based implementation.

- [X] T004 [US1] Update the PDF fixture and assertions in `backend/tests/test_payment_receipt.py` to set a known `payment_identifier`, assert the identifier and translated label appear in extracted PDF text, and assert the legacy `reference` value is not used as the receipt identifier.
- [X] T005 [US1] Add an isolated projection assertion in `backend/tests/test_payment_receipt.py` for `build_receipt()` to require an `identifier` value sourced from `Payment.payment_identifier` while preserving existing reservation and empty-state data.

### Implementation for User Story 1

- [X] T006 [US1] Update `build_receipt()` and `render_pdf()` in `backend/apps/payments/receipt.py` to expose and render the public `payment_identifier` in the localized receipt header/reference area instead of `payment.reference`, without changing the reservation query or other header values.
- [X] T007 [US1] Run the focused PDF tests in `backend/tests/test_payment_receipt.py` and confirm User Story 1 passes with the existing authenticated route in `backend/apps/payments/api_urls.py`.

**Checkpoint**: PDF receipts independently identify the selected payment with `payment_identifier` and preserve all existing receipt data.

---

## Phase 4: User Story 2 - Download Consistently Named Receipt Files (Priority: P1)

**Goal**: Use the sanitized client name and public payment identifier in PDF download filenames.

**Independent Test**: Download a PDF for a payment whose identifier contains whitespace and path-sensitive punctuation, then verify the attachment filename contains only sanitized client/identifier components and never the legacy reference.

### Tests for User Story 2

> Write these tests first and confirm they fail against the current reference-based filename.

- [X] T008 [US2] Replace the reference-based filename assertions in `backend/tests/test_payment_receipt.py` with the `payment_<client>_<payment_identifier>.pdf` convention and assert the legacy reference is absent from `Content-Disposition`.
- [X] T009 [US2] Add filename-sanitization cases in `backend/tests/test_payment_receipt.py` for spaces, slashes, control characters, accented client names, and empty/unsafe components, asserting a non-empty path-safe filename.

### Implementation for User Story 2

- [X] T010 [US2] Update the filename construction in `backend/apps/payments/receipt.py` to pass `payment.payment_identifier` through `_safe_filename_part()` and produce the required `.pdf` attachment name while retaining the existing sanitizer and fallback behavior.
- [X] T011 [US2] Run the focused filename and authenticated PDF endpoint tests in `backend/tests/test_payment_receipt.py`, including the existing 50-reservation performance case, and confirm no extra receipt-data query or generation regression is introduced.

**Checkpoint**: PDF downloads are recognizable, sanitized, and safe without changing the endpoint or calendar action.

---

## Phase 5: User Story 3 - Keep Markdown Output Aligned (Priority: P2)

**Goal**: Ensure the existing copyable Markdown receipt contains the same public payment identifier as the PDF.

**Independent Test**: Request the authenticated Markdown endpoint, decode the response, and verify the public identifier and translated label match the PDF projection while reservation and empty-state content remain intact.

### Tests for User Story 3

> Write these tests first and confirm they fail because the current Markdown output has no payment identifier.

- [X] T012 [US3] Extend Markdown assertions in `backend/tests/test_payment_receipt.py` to require the known `payment_identifier` and translated label, and to reject the legacy reference as the receipt identifier.
- [X] T013 [US3] Add an empty-payment Markdown assertion in `backend/tests/test_payment_receipt.py` that verifies the identifier remains present alongside the localized no-reservations message.

### Implementation for User Story 3

- [X] T014 [US3] Update `render_markdown()` in `backend/apps/payments/receipt.py` to render the shared public identifier and label using the same projection consumed by the PDF, without adding a new Markdown download endpoint.
- [X] T015 [US3] Run the focused Markdown endpoint tests in `backend/tests/test_payment_receipt.py` and verify the existing clipboard/fallback UI contract in `backend/apps/payments/templates/payments/payment_detail.html` remains unchanged.

**Checkpoint**: PDF and copyable Markdown outputs identify the same payment and preserve localized reservation content.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate regression safety, constitutional requirements, and the documented interface contract.

- [X] T016 [P] Review `specs/068-update-payment-identifier/contracts/receipt-downloads.md`, `specs/068-update-payment-identifier/data-model.md`, and `specs/068-update-payment-identifier/quickstart.md`; no changes are required because the final projection and validation commands match the plan.
- [X] T017 [P] Add or update regression assertions in `backend/tests/test_payment_detail_template.py` and `backend/tests/test_payments_calendar.py` to prove the receipt action remains before the calendar action and calendar downloads still use their existing payment-identifier behavior.
- [X] T018 Run the complete validation suite with `uv run pytest backend/tests`, run Ruff against changed Python files, and verify no migration files or dependency changes were introduced in `backend/apps/payments/migrations/` or `backend/pyproject.toml`.
- [X] T019 Validate the automated scenarios in `specs/068-update-payment-identifier/quickstart.md`, including unsafe filename sanitization, active-language receipt content, Markdown output, and calendar regression; browser-only clipboard fallback remains covered by the existing template contract tests.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies; T001 and T002 can run in parallel.
- **Phase 2 (Foundational)**: Depends on Phase 1; T003 can proceed after the scope check and blocks receipt-rendering implementation.
- **Phase 3 (US1)**: Depends on Phase 2; tests T004-T005 must fail before T006, then T007 validates the story.
- **Phase 4 (US2)**: Depends on US1 because filename data is part of the shared receipt projection in `backend/apps/payments/receipt.py`; tests T008-T009 must fail before T010, then T011 validates the story.
- **Phase 5 (US3)**: Depends on US1 and the shared projection shape; tests T012-T013 must fail before T014, then T015 validates the story.
- **Phase 6 (Polish)**: Depends on all desired user stories; T016-T019 complete documentation, regression, lint, full-suite, and manual validation.

### User Story Dependencies

- **US1 (P1)**: Depends only on the foundational translation/scope checks and is the MVP.
- **US2 (P1)**: Depends on US1 because it consumes the updated receipt projection and shares `receipt.py` and `test_payment_receipt.py`.
- **US3 (P2)**: Depends on US1 because it consumes the updated receipt projection; execute after US2 to avoid concurrent edits to shared files.

### Parallel Opportunities

- T001 and T002 can run in parallel during setup.
- T003 is independent of the baseline test run once the scope is confirmed.
- T004 and T005, T008 and T009, and T012 and T013 are intentionally sequential because each pair edits the same `backend/tests/test_payment_receipt.py` file.
- T016 and T017 can run in parallel after story implementation because they touch separate documentation/test files.
- Do not implement US1, US2, and US3 concurrently: they all modify `backend/apps/payments/receipt.py` and the same receipt test module.

## Parallel Example: Setup and Polish

```text
Task: T001 Run the baseline receipt, template, and calendar tests in backend/tests/.
Task: T002 Confirm the migration-free scope in backend/apps/payments/models.py, backend/apps/payments/api_urls.py, and backend/pyproject.toml.
```

```text
Task: T016 Reconcile the receipt contract, data model, and quickstart documentation under specs/068-update-payment-identifier/.
Task: T017 Add calendar and payment-detail regression assertions in backend/tests/test_payment_detail_template.py and backend/tests/test_payments_calendar.py.
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write and fail T004-T005.
3. Implement T006 and run T007.
4. Stop and validate that PDF receipts display `payment_identifier` without the legacy reference.

### Incremental Delivery

1. Add US1 to replace the visible PDF identifier and validate it independently.
2. Add US2 to replace and sanitize the PDF filename, then validate download and performance behavior.
3. Add US3 to align copyable Markdown content.
4. Complete cross-cutting regression, lint, full-suite, and manual checks.

### Environment Reference

- **Run targeted/full tests**: `uv run pytest backend/tests/test_payment_receipt.py` or `uv run pytest backend/tests`
- **Run migrations**: Not applicable; this feature has no migration task.
- **Install packages**: Not applicable; no dependency changes are planned.
- **Lint changed Python files**: Use the repository’s configured Ruff command against changed files.

## Notes

- Every implementation task names its target file path.
- Tests are explicitly first within each story and must be reviewed/failing before implementation per the constitution.
- `[P]` is used only where work can be isolated without an incomplete dependency; shared-file test edits require coordination.
- No model, URL, endpoint, dependency, or Markdown download task is included because the design preserves those boundaries.
