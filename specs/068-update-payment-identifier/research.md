# Research: Payment Receipt Identifier Integration

## Decision: Reuse the existing normalized receipt projection

- **Decision**: Change the existing `build_receipt(payment)` projection so its public identifier is sourced from `payment.payment_identifier`, then let both `render_pdf()` and `render_markdown()` consume that value.
- **Rationale**: The current module already centralizes client, payment, reservation, localized labels, and filename data. Updating one projection prevents PDF and Markdown from diverging.
- **Alternatives considered**: Adding separate PDF and Markdown mappings was rejected because it would duplicate the same business rule and make inconsistent identifiers more likely.

## Decision: Replace the visual reference rather than display both values

- **Decision**: Add a translated payment-identifier label to the receipt header/reference area and remove the legacy `reference` value from the rendered receipt representations.
- **Rationale**: The feature specification defines `payment_identifier` as the public identifier and explicitly treats the old reference as replaced in the visual layout.
- **Alternatives considered**: Displaying both values was rejected because it preserves ambiguity and does not satisfy the replacement requirement.

## Decision: Keep the current Markdown action as clipboard output

- **Decision**: Update Markdown text content only. Do not add a separate Markdown download response or filename in this change.
- **Rationale**: The current payment detail action calls the Markdown endpoint, reads text, and copies it to the clipboard with a manual-copy fallback. The specification makes Markdown filename behavior conditional on a downloadable Markdown output, which does not currently exist.
- **Alternatives considered**: Adding a new Markdown download action was rejected as scope expansion unrelated to replacing the identifier.

## Decision: Reuse and test the existing filename sanitizer

- **Decision**: Continue sanitizing client name and payment identifier through `_safe_filename_part()` before constructing the PDF attachment filename. Add tests for separators, whitespace, control characters, and empty components.
- **Rationale**: The helper already replaces unsafe filename characters and whitespace and falls back to `unknown`; keeping it avoids introducing a second security-sensitive implementation.
- **Alternatives considered**: Using an external filename library or changing the normalization policy was rejected because no new dependency is needed and the existing behavior preserves accented letters as required by the prior receipt feature.

## Decision: Preserve HTTP, authentication, and query boundaries

- **Decision**: Keep `/api/payments/<id>/receipt/`, `/api/payments/<id>/receipt/markdown/`, `@login_required`, the selected-payment lookup, and the existing reservation query unchanged.
- **Rationale**: This is a representation change, not a new integration. Existing Django download response and authentication patterns are already in use and align with current documentation.
- **Alternatives considered**: Introducing new routes or changing authorization boundaries was rejected because it would increase regression risk without contributing to the requested identifier update.

## Resolved Technical Unknowns

- The project targets Python 3.12+ and Django 5.0.x from `backend/pyproject.toml`.
- ReportLab and pdfminer.six are already declared dependencies; no dependency research or package change is needed.
- The payment identifier is a unique, human-readable `Payment.payment_identifier` field with a maximum length of 50; no data migration is required.
- The existing PDF endpoint returns an attachment with `Content-Disposition`; the Markdown endpoint returns copyable `text/markdown` content without an attachment filename.
