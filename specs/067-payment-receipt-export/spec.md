# Feature Specification: Payment Receipt Export

**Feature Branch**: `067-payment-receipt-export`

**Created**: 2026-08-12

**Status**: Draft

**Input**: User description: "Payment Receipt Generation & Export"

## Clarifications

### Session 2026-08-12

- Q: Should the PDF and Markdown receipt content be generated in Spanish, English, or based on the operator’s active language? → A: Match the operator’s active language.
- Q: How should client names be normalized in the PDF filename when they contain accents, punctuation, or other non-ASCII characters? → A: Keep accented letters; replace spaces and unsafe characters with underscores.
- Q: What should the filename use when a payment has no populated payment reference? → A: Use payment ID.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download a payment receipt (Priority: P1)

As an operator, I want to download a formal receipt for a specific payment from its details page so that I can provide proof of payment and keep accurate records.

**Why this priority**: A reliable receipt is the primary business value of the feature and must be available directly where the operator reviews a payment.

**Independent Test**: Open a payment with reservations, activate the receipt download action, and verify that a readable file is downloaded with the payment and reservation details.

**Acceptance Scenarios**:

1. **Given** an operator is viewing a payment detail page, **When** the page loads, **Then** a button labeled "Descargar pago" appears immediately to the left of "Descargar calendario".
2. **Given** a payment has associated reservations, **When** the operator selects "Descargar pago", **Then** a PDF receipt downloads with the client, amount, payment type, payment date, class-slot count, and an associated-reservations table.
3. **Given** receipt generation is in progress, **When** the operator waits for the download, **Then** the action visibly indicates loading and prevents duplicate requests until generation completes or fails.
4. **Given** receipt generation fails, **When** the failure is reported, **Then** the operator sees an actionable error and can retry without leaving the payment detail page.

---

### User Story 2 - Share receipt content (Priority: P2)

As an operator, I want to copy the receipt content in Markdown so that I can paste a structured payment summary into another record or message.

**Why this priority**: Sharing the receipt content provides a lightweight alternative when sending or storing a PDF is inconvenient.

**Independent Test**: Open a payment detail page, activate the adjacent Markdown copy action, and paste the result into a plain-text editor to verify its structure and values.

**Acceptance Scenarios**:

1. **Given** an operator is viewing a payment detail page, **When** the page loads, **Then** a Markdown receipt action appears adjacent to the PDF download action.
2. **Given** the payment has any number of associated reservations, **When** the operator selects the Markdown action, **Then** the complete receipt content is copied in Markdown, including the header information and reservations table or the stated empty result.
3. **Given** clipboard access is unavailable, **When** the operator selects the Markdown action, **Then** the receipt content remains available for manual copying through a visible fallback.

### Edge Cases

- A payment with zero associated reservations shows the localized equivalent of "No reservations found" in the receipt table instead of an empty or broken table.
- A client name containing spaces or filesystem-sensitive characters is converted into a safe filename by preserving accented letters and replacing spaces or unsafe characters with underscores, while preserving the payment reference.
- A payment without a populated reference uses its unique payment ID in the filename.
- A payment that no longer exists cannot produce a receipt; the operator receives a not-found message and no file is downloaded.
- A payment with a missing optional equipment value displays a clear empty value rather than failing receipt generation.
- A payment with more than 50 reservations remains usable; the receipt may span multiple pages and retains every reservation row.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The payment details page MUST provide a "Descargar pago" action positioned to the left of the existing "Descargar calendario" action.
- **FR-002**: The receipt action MUST generate and download a PDF for the payment currently being viewed.
- **FR-003**: The PDF MUST identify the client, total amount, payment type, payment date, and number of class slots.
- **FR-004**: The PDF MUST include a structured table with class slot, date in `DD/MM/YYYY` format, equipment, and reservation status for every reservation associated with the payment.
- **FR-005**: When no reservations are associated with the payment, the PDF and Markdown receipt MUST display the localized equivalent of "No reservations found".
- **FR-006**: The downloaded PDF filename MUST follow `payment_<client_name>_<payment_reference>.pdf`, with spaces and unsafe filename characters replaced by underscores while preserving accented letters; if the payment reference is missing, the payment ID MUST be used as `<payment_reference>`.
- **FR-007**: The payment details page MUST provide a Markdown receipt action adjacent to the PDF action.
- **FR-008**: The Markdown receipt MUST contain the same localized header information and reservation rows as the PDF in a copy-pasteable format.
- **FR-009**: Receipt actions MUST provide visible progress feedback while generating or preparing content, prevent duplicate activation during that operation, and provide an actionable retry path after failure.
- **FR-010**: Receipt generation MUST be available only to operators who can view the payment details page.
- **FR-011**: Receipt data MUST correspond only to the selected payment and its associated client and reservations.

### Key Entities

- **Payment**: The selected financial transaction, including its reference, amount, payment type, date, client, and associated class-slot count.
- **Client**: The person or organization who made the payment and whose name appears in the receipt and filename.
- **Reservation**: A class booking linked to the payment, including its class slot, date, equipment, and current status.
- **Payment Receipt**: A derived representation of one payment and its associated reservations, available as PDF and Markdown content.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can start a PDF receipt download from any accessible payment detail page in one action.
- **SC-002**: At least 95% of receipt requests for payments with up to 50 reservations produce a usable PDF within 10 seconds.
- **SC-003**: 100% of generated receipts contain the five required localized header fields and exactly one row for each associated reservation, or the localized no-reservations message.
- **SC-004**: 100% of generated filenames match the required payment naming pattern and remain valid for common desktop file systems.
- **SC-005**: Operators can copy a complete Markdown receipt in the operator’s active language, including the localized empty-state message where applicable, in under 30 seconds.
- **SC-006**: In usability checks, at least 90% of operators identify and successfully use the PDF action without assistance.

## Assumptions

- Operators already have permission to view payment details and their associated reservations.
- The existing payment reference is unique enough to distinguish receipts for the same client.
- The payment ID is unique and available as a fallback when a payment reference is missing.
- The PDF and Markdown actions use the current payment detail page as their only payment selection mechanism.
- Markdown is copied to the clipboard with a visible fallback for browsers that deny clipboard access; a separate Markdown file download is not required for the first release.
- Receipt generation is synchronous for the expected volume, while large reservation sets must remain readable across multiple pages.
- Receipt labels, date, amount, payment-type, reservation-status, and empty-state text are generated in the operator’s active language using the application’s existing localization conventions.
