# Receipt API Contract

## PDF Receipt

`GET /api/payments/{id}/receipt/`

Authentication: required. The caller must have access to the payment detail page.

Success `200`:

- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="payment_<client>_<reference>.pdf"`
- Body: binary PDF containing localized payment header fields and the associated reservation table.

The `<reference>` component is the payment reference when populated, otherwise the payment ID. Client-name spaces and unsafe filename characters are replaced with underscores; accented letters are preserved.

Error responses:

- `302` to the login page for an unauthenticated browser request, following the project’s existing authenticated-view behavior.
- `404` when the payment does not exist or is not available to the current detail view.
- `500` with a localized actionable error response/redirect when PDF generation fails, without returning a partial PDF.

## Markdown Receipt

`GET /api/payments/{id}/receipt/markdown/`

Authentication: required. The same payment access boundary and data projection as the PDF route apply.

Success `200`:

- `Content-Type: text/markdown; charset=utf-8`
- Body: localized Markdown receipt containing the same header fields and reservation rows as the PDF.
- A zero-row receipt includes the localized equivalent of "No reservations found".

Error responses follow the PDF contract for authentication and missing payments. The payment detail page exposes a copy action and a visible text fallback when browser clipboard access fails.

## Page Contract

On `/payments/{id}/`:

- `Descargar pago` appears immediately left of `Descargar calendario`.
- A Markdown copy action appears adjacent to the PDF action.
- PDF generation shows loading state and prevents duplicate activation.
- Markdown copy shows success feedback or exposes text for manual copying.
