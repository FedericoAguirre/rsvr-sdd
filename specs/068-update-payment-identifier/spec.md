# Feature Specification: Payment Receipt Identifier Integration

**Feature Branch**: `068-update-payment-identifier`

**Created**: 2026-08-12

**Status**: Draft

**Input**: User description: "Replace payment_reference with payment_identifier in payment receipt content and downloadable PDF/Markdown filenames, while preserving existing payment-page behavior."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identify the payment receipt (Priority: P1)

As a staff member viewing a payment receipt, I want the receipt to show the payment's public identifier so that I can unambiguously match the document to the payment.

**Why this priority**: The identifier is the primary business value of this change and must be consistent in every receipt representation.

**Independent Test**: Generate a receipt for a payment with a known public identifier and verify that the identifier is visible in the document while the former reference is not used as the displayed receipt identifier.

**Acceptance Scenarios**:

1. **Given** a payment has a public `payment_identifier`, **When** its receipt is generated as a PDF, **Then** the PDF clearly displays that identifier in the receipt header or reference area.
2. **Given** a payment has both a `payment_identifier` and a `payment_reference`, **When** its receipt is generated, **Then** the visible reference value is the `payment_identifier` and not the `payment_reference`.

---

### User Story 2 - Download consistently named receipt files (Priority: P1)

As a staff member downloading a receipt, I want the filename to contain the public payment identifier so that I can recognize the file without opening it.

**Why this priority**: A misleading or inconsistent filename makes payment documents difficult to organize and retrieve.

**Independent Test**: Download a PDF receipt for a payment with spaces and special characters in its identifier and inspect the resulting filename.

**Acceptance Scenarios**:

1. **Given** a payment has client name `Client Name` and identifier `PAY/2026 001`, **When** the PDF is downloaded, **Then** its filename follows `payment_<client>_<payment_identifier>.pdf` using a safe sanitized form of each variable and contains no path separators or unsafe special characters.
2. **Given** a payment identifier is available, **When** the PDF download is requested, **Then** the filename does not contain the payment reference.

---

### User Story 3 - Keep Markdown output aligned (Priority: P2)

As a staff member using the optional Markdown receipt output, I want its content and filename to identify the same payment as the PDF.

**Why this priority**: Different identifiers across output formats create ambiguity when receipts are shared or archived.

**Independent Test**: Generate or download Markdown output for a known payment and verify its content and filename use the public identifier.

**Acceptance Scenarios**:

1. **Given** Markdown receipt output is available, **When** it is generated, **Then** its text includes the `payment_identifier` and does not use `payment_reference` as the receipt identifier.
2. **Given** Markdown receipt output is downloadable, **When** it is downloaded, **Then** its filename follows the same sanitized base convention as the PDF and ends in `.md`.

### Edge Cases

- A payment identifier containing spaces, path separators, punctuation, or other filename-sensitive characters is normalized to a safe filename component without allowing directory traversal.
- A payment identifier containing accented or other non-ASCII characters remains readable in the receipt content, while the filename uses a safe normalized representation.
- If the optional Markdown output is not enabled or available, the PDF behavior remains complete and is not blocked by the Markdown requirements.
- Existing payment-page actions, including downloading the calendar, remain available and behave as before.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The receipt MUST include the payment's `payment_identifier` in a clearly labeled reference area in the PDF output.
- **FR-002**: The PDF receipt MUST replace the displayed `payment_reference` value with `payment_identifier`; the former reference MUST NOT be presented as the receipt's public identifier.
- **FR-003**: The receipt-generation data supplied to each output MUST include the payment identifier associated with the selected payment.
- **FR-004**: The PDF download filename MUST use the pattern `payment_<client>_<payment_identifier>.pdf` rather than the payment reference.
- **FR-005**: The Markdown receipt content MUST include the payment identifier whenever Markdown output is available.
- **FR-006**: A downloadable Markdown receipt MUST use the pattern `payment_<client>_<payment_identifier>.md` rather than the payment reference.
- **FR-007**: Every client-name and payment-identifier component used in a downloadable filename MUST be sanitized to remove or replace path separators, whitespace, and filename-unsafe characters before the filename is returned.
- **FR-008**: Filename sanitization MUST prevent path traversal and MUST produce a valid non-empty filename for ordinary valid payment and client data.
- **FR-009**: The change MUST preserve the existing payment page, including the calendar download action and access controls.

### Key Entities

- **Payment**: The transaction whose receipt is generated; includes the public `payment_identifier` and the legacy `payment_reference` that is no longer used as the displayed or filename identifier.
- **Client**: The customer associated with the payment; contributes a sanitized name component to downloadable receipt filenames.
- **Receipt Output**: A PDF, and optionally a Markdown document, representing one payment and its identifier.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of generated PDF receipts for payments with a valid identifier display the `payment_identifier` and do not display `payment_reference` as the public receipt reference.
- **SC-002**: 100% of PDF downloads use a sanitized filename containing the client component and payment identifier, with the `.pdf` extension.
- **SC-003**: 100% of available Markdown receipts include the same payment identifier as the PDF; 100% of downloadable Markdown files use the corresponding `.md` filename convention.
- **SC-004**: At least 95% of staff completing a receipt-download usability check can identify the payment from the downloaded filename without opening the file.
- **SC-005**: The existing calendar download action remains usable in 100% of regression checks on the payment page.

## Assumptions

- Staff users already have access to the existing payment detail and receipt-download actions.
- `payment_identifier` is the intended human-readable public identifier; no new identifier format or database field is introduced by this request.
- The change replaces the legacy reference in the visual receipt and download naming rather than displaying both values.
- Markdown output is optional; requirements for its filename apply only where that output is currently offered for download.
- Existing receipt layout, language behavior, payment data, permissions, and calendar functionality remain in scope and must not regress.
