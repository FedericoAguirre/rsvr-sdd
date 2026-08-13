# Quickstart: Payment Receipt Export

## Prerequisites

- From the repository root, start PostgreSQL with `make db-up` if local database data is required.
- Use the project environment and run commands through `uv`.
- Have an authenticated operator account.
- Have one payment with at least one linked reservation and one payment with no linked reservations.

## Automated Validation

From the `backend/` directory:

```bash
uv run pytest tests/test_payment_receipt.py tests/test_payment_detail_template.py
```

Expected results:

- Authenticated receipt requests return the documented PDF or Markdown content type.
- PDF headers contain client, amount, payment type, date, class-slot count, and reservation rows.
- Empty payments include the localized no-reservations message.
- Filenames preserve accented client letters, replace unsafe characters, and fall back to payment ID when needed.
- Unauthenticated and missing-payment requests are handled without data leakage.
- The detail page contains the receipt actions in the required order.

## Manual End-to-End Validation

1. Sign in and open `/payments/<id>/` for a payment with linked reservations.
2. Confirm `Descargar pago` is immediately left of `Descargar calendario`.
3. Select the PDF action and verify the download filename and all table rows.
4. Return to the detail page and select the Markdown action.
5. Paste into a Markdown-capable editor; verify the same localized values as the PDF.
6. Disable or deny clipboard access and verify the visible manual-copy fallback.
7. Repeat with a payment that has no reservations and verify the localized empty-state message.
8. Repeat with an accented/punctuated client name and an empty optional payment reference.

## Performance Validation

The automated suite includes a representative 50-reservation request and asserts completion within 10 seconds. The latest feature-suite run completed in 1.56 seconds total, including that request.

See [receipt-api.md](./contracts/receipt-api.md) for response and error contracts and [data-model.md](./data-model.md) for projection invariants.
