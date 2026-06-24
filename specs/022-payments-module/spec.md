# Feature Specification: Payments Module

**Feature Branch**: `022-payments-module`

**Created**: 2026-06-24

**Status**: Draft

**Input**: User description: "from the @ai/features/todos/08_add_payments_module.md create the specs for the new feature"

## Clarifications

### Session 2026-06-24

- Q: Role Permissions — Are "operator" and "administrator" distinct roles with permission enforcement? → A: Two distinct roles — operators can create, edit, delete payments and view client payment history; administrators inherit all operator capabilities plus access to payment reports.
- Q: Payment Lifecycle — Can payments be edited or deleted after creation? → A: Limited edit (reference, notes, evidence only) + soft delete with audit trail. Amount, type, client, and identifier are locked after creation.
- Q: Data Volume — How many payments does the business process? → A: Moderate volume — 50-200 payments per month.
- Q: Payment-Reservation Association — How does the association workflow work in practice? → A: Two-step flow on New Reservations page: create payment first, then select which of the client's existing reservations to link.

## User Scenarios & Testing

### User Story 1 - Register a Client Payment (Priority: P1)

As an operator, I want to register a payment made by a client so that the payment information is recorded in the system instead of a spreadsheet.

**Why this priority**: This is the core functionality of the module — without being able to record payments, the module provides no value. It replaces the current manual spreadsheet workflow.

**Independent Test**: Can be fully tested by creating a new payment record and verifying all entered data is saved and visible. Delivers the ability to digitize payment records.

**Acceptance Scenarios**:

1. **Given** I am on the payments page, **When** I fill in the payment form with valid data (date, client, payment type, identifier, amount, class slot count) and submit, **Then** the payment is saved and I can see it in the list.
2. **Given** I am on the payments page, **When** I submit the form with a missing required field (e.g., no amount), **Then** I see an error message and the payment is not saved.
3. **Given** I am creating a payment from the New Reservations page, **When** I complete the payment form and submit, **Then** the payment is saved and I can associate it with reservations.
4. **Given** I have created a payment, **When** I optionally attach an evidence image, a reference, and notes, **Then** these optional fields are saved and visible in payment details.

---

### User Story 2 - View Client Payment History (Priority: P2)

As an operator, I want to view the payment history of a specific client so that I can quickly see what a client has paid and when.

**Why this priority**: Operators need to verify client payments during check-in or when answering client inquiries. Essential for daily operations.

**Independent Test**: Can be fully tested by navigating to a client's payment history and verifying the list shows payments ordered by date with correct pagination. Delivers visibility into client payment records.

**Acceptance Scenarios**:

1. **Given** a client has multiple payments recorded, **When** I view their payment history, **Then** I see payments sorted by date in descending order (most recent first).
2. **Given** a client has more than 5 payments, **When** I view their payment history, **Then** I see the first 5 payments and can navigate to subsequent pages.
3. **Given** a client has no payments, **When** I view their payment history, **Then** I see a message indicating no payments found.

---

### User Story 3 - Associate Payment with Reservations (Priority: P3)

As an operator, I want to link a client's payment to their reservations so that the system knows which reservations are covered by which payment. The association is a two-step flow: create payment first, then select reservations to link.

**Why this priority**: This integration connects payments to the existing reservation workflow, enabling accurate tracking of paid reservations.

**Independent Test**: Can be fully tested by creating a payment and associating it with N reservations. Delivers the link between payments and the class slots they cover.

**Acceptance Scenarios**:

1. **Given** I am on the New Reservations page and have created a payment, **When** I select from a list of that client's existing reservations and link them, **Then** the payment shows as linked to those reservations.
2. **Given** I have created a payment with a class slot count of 3, **When** I try to associate it with 3 reservations for that client, **Then** the association succeeds.
3. **Given** I have created a payment with a class slot count of 3, **When** I try to associate it with more than 3 reservations, **Then** the system prevents the association with an appropriate message.
4. **Given** a payment is already associated with some reservations, **When** I view the payment details, **Then** I can see which reservations are linked.

---

### User Story 4 - View Payment Reports (Priority: P4)

As an administrator, I want to see payments summarized by day, week, month, or custom date range and grouped by payment type so that I can understand revenue patterns. (Operator role does not have access to reports.)

**Why this priority**: Reporting provides business intelligence value but is not required for the core payment recording workflow. Can be developed after the basic payment operations are stable.

**Independent Test**: Can be fully tested by selecting different date ranges and payment type groupings and verifying the aggregated totals are correct. Delivers business analytics capability.

**Acceptance Scenarios**:

1. **Given** there are payments recorded on multiple dates, **When** I select a weekly summary, **Then** I see payments grouped by week with totals for amount, reservation count, and payment count.
2. **Given** there are payments of different types, **When** I view the report, **Then** the summary is grouped by payment type showing subtotals for each.
3. **Given** I select a custom date range, **When** I generate the report, **Then** only payments within that range are included.
4. **Given** I am logged in as an operator (not administrator), **When** I try to access the reports page, **Then** I see an access denied message.

---

### Edge Cases

- What happens when a payment's client is deleted or deactivated? Payments should remain as historical records.
- How does the system handle the payment identifier when no payments exist for a given day? The consecutive counter starts at 001.
- How does the system handle duplicate payment identifiers? The system should enforce uniqueness of the payment identifier.
- What happens when evidence image upload fails (exceeds size, wrong format)? User receives a clear error message; the payment can still be saved without evidence.
- How does the system handle associating a payment to reservations that already have a different payment linked? The system should handle this gracefully, either allowing reassignment or showing a warning.
- Can an operator edit a payment after creation? Only reference, notes, and evidence can be edited. Amount, payment type, client, and identifier are locked after creation.
- Can a payment be deleted? Payments can be soft-deleted (flagged as deleted but preserved for audit trail). Hard deletion is not allowed.
- What happens to reservations associated with a soft-deleted payment? The association should be preserved in the audit record, and the reservations may need to be reassigned or flagged as unpaid.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST allow operators to register a payment with the following required fields: date, client, payment type, payment identifier, amount, and class slot count.
- **FR-002**: The system MUST allow operators to optionally add a reference, evidence image, and notes to a payment.
- **FR-003**: The system MUST support the following payment types: cash, credit card, debit card, electronic transfer, and payments app.
- **FR-004**: The system MUST auto-generate the payment identifier using the format: payment type acronym (2-3 letters) + date (YYYYMMDD) + client initials + 3-digit consecutive number (reset daily per payment type).
- **FR-005**: The system MUST enforce that the payment identifier is unique across all payments.
- **FR-006**: The system MUST record audit timestamps (created at, updated at) and the operator who created or last modified each payment.
- **FR-007**: The system MUST display a paginated list of payments per client, with 5 payments per page, ordered by descending date.
- **FR-008**: The payments module MUST be accessible from the main menu, alongside other modules.
- **FR-009**: Operators MUST be able to create a new payment from the New Reservations page.
- **FR-009a**: The system MUST enforce two distinct roles: operator and administrator. Operators can create, view, edit, and delete payments and view client payment history. Administrators inherit all operator capabilities and additionally can access payment reports.
- **FR-010**: A payment MUST exist in the system before it can be associated with reservations.
- **FR-011**: Operators MUST be able to associate a payment with up to N reservations, where N equals the payment's class slot count.
- **FR-012**: The system MUST prevent associating a payment with more reservations than its class slot count.
- **FR-013**: Administrators MUST be able to view payment summaries grouped by day, week, month, or custom date range.
- **FR-014**: Payment summaries MUST group data by payment type and show aggregated amount, reservation count, and payment count.
- **FR-015**: Payment reports SHOULD include basic graphical charts to visualize the aggregated data.
- **FR-016**: The system MUST generate the 3-digit consecutive number independently per day and per payment type, starting at 001 for the first payment of a given type on a given day.
- **FR-017**: After a payment is created, only the following fields MAY be edited: reference, notes, and evidence. Amount, payment type, client, date, and identifier MUST be locked.
- **FR-018**: Operators MUST be able to soft-delete a payment (flag as deleted while preserving the record). Hard deletion MUST NOT be allowed.
- **FR-019**: The system MUST record which operator performed an edit or soft-delete, and the timestamp of the action (audit trail).

### Key Entities

- **Payment**: Represents a financial transaction made by a client. Contains date, payment type, payment identifier, amount, class slot count, optional reference, optional evidence image, optional notes, audit timestamps, and created/updated by operator. Linked to a client and can be associated with multiple reservations.
- **Payment Type**: Classification of the payment method (cash, credit card, debit card, electronic transfer, payments app). Determines the acronym used in the payment identifier.
- **Payment-Client Relationship**: Each payment belongs to exactly one client. A client can have multiple payments.
- **Payment-Reservation Relationship**: A payment can be linked to multiple reservations (one-to-many), limited by the class slot count. Each reservation belongs to at most one payment.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Operators can register a new client payment in under 2 minutes using the interface.
- **SC-002**: Operators can find and view a specific client's payment history within 3 clicks or less from the main menu.
- **SC-003**: Payment identifier auto-generation produces unique identifiers with zero collisions in normal operation.
- **SC-004**: Administrators can generate a payment summary report for any date range within 2 clicks.
- **SC-005**: The payment-to-reservation association workflow can be completed within 30 seconds for a typical case (3-5 reservations).
- **SC-006**: At least 95% of payment records entered through the system require no manual correction or spreadsheet cross-reference.

## Assumptions

- Evidence images will be standard web image formats (JPEG, PNG) with a reasonable size limit (up to 5MB per image).
- The payment identifier auto-generation may be overridden by the operator if needed for manual corrections.
- Operators are logged in and authenticated through the existing system authentication.
- Reports will be rendered in-browser; PDF or print export is out of scope for v1.
- Multiple payments can exist for the same client on the same day, each with a unique identifier.
- The existing client account system is used to select the client when creating a payment.
- Online payments and payments broker integrations are out of scope for this feature (future phases).
- The New Reservations page is an existing feature that will be extended to support payment creation and association.
- Expected payment volume is moderate: 50-200 payments per month total across all clients. The 5-items-per-page pagination is appropriate for this volume.
