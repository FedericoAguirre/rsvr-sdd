# Quickstart: Payment Receipt Identifier Integration

## Prerequisites

- POSIX shell with the repository checkout on branch `068-update-payment-identifier`.
- Python dependencies installed through the project environment.
- PostgreSQL available using the project’s normal development setup.

## Automated Validation

Run from the repository root:

```bash
uv run pytest backend/tests/test_payment_receipt.py backend/tests/test_payment_detail_template.py backend/tests/test_payments_calendar.py
```

Expected results:

- PDF receipt tests find `payment_identifier` in extracted PDF text.
- PDF `Content-Disposition` uses the sanitized client and payment identifier, never the legacy payment reference.
- Markdown content includes the same identifier and preserves localized reservation/empty-state text.
- Unauthenticated and missing-payment behavior remains protected.
- The 50-reservation receipt remains under the existing 10-second target.
- Receipt and calendar actions remain present and ordered correctly.

Run the full backend suite before implementation is considered complete:

```bash
uv run pytest backend/tests
```

Also run repository formatting/lint checks according to the project’s normal CI commands, including Ruff for changed Python files.

## Manual Validation

1. Start the application using the project’s normal local setup and sign in as an operator.
2. Open a payment detail page with a known `payment_identifier` and a different populated `reference`.
3. Select **Descargar pago** and confirm the PDF displays the payment identifier in its reference area.
4. Confirm the downloaded filename uses `payment_<client>_<payment_identifier>.pdf`; test an identifier containing whitespace and path-sensitive punctuation.
5. Select **Copiar comprobante**, paste the result into a text editor, and confirm the Markdown includes the same identifier.
6. Select **Descargar calendario** and confirm it still downloads the calendar as before.

Refer to [receipt-downloads.md](contracts/receipt-downloads.md) for the expected HTTP and UI contract details and [data-model.md](data-model.md) for the projection rules.
