# Receipt Download Contracts

These contracts describe the existing user-facing interfaces that the implementation must preserve while changing the receipt identifier.

## PDF Receipt

- **Route**: `GET /api/payments/{payment_id}/receipt/`
- **Access**: Authenticated users only; unauthenticated requests retain the existing login redirect behavior.
- **Success**: HTTP `200`, `Content-Type: application/pdf`, and `Content-Disposition: attachment`.
- **Filename**: `payment_<sanitized_client>_<sanitized_payment_identifier>.pdf`.
- **Content**: Localized receipt title, client, amount, payment type, date, class-slot count, public payment identifier, and all associated reservation rows. Empty associations show the localized empty-state message.
- **Failure**: Existing JSON error response and HTTP status behavior remain unchanged.

## Markdown Receipt

- **Route**: `GET /api/payments/{payment_id}/receipt/markdown/`
- **Access**: Authenticated users only; same payment selection boundary as the PDF route.
- **Success**: HTTP `200`, `Content-Type: text/markdown; charset=utf-8`, and Markdown text suitable for clipboard copying.
- **Content**: The same localized header values as the PDF, including the public payment identifier, plus the same reservation rows or localized empty-state message.
- **Download filename**: Not applicable to the current contract because the payment detail action copies the response rather than downloading a Markdown file. If a future downloadable Markdown action is added, it must use the PDF filename base and `.md` extension.

## Payment Detail UI

- The existing PDF receipt action remains adjacent to and before the calendar download action.
- The existing Markdown copy action, loading state, error state, and manual-copy fallback remain available.
- The calendar download action remains available and continues to use the payment identifier in its existing calendar filename/metadata behavior.
