# Feature Specification: Fix PaymentReservation ForeignKey Warning

**Feature Branch**: `060-fix-payment-fk-warning`

**Created**: 2026-08-02

**Status**: Draft

**Input**: User description: "Remove the Django warning `fields.W342` on `payments.PaymentReservation.reservation`: Setting `unique=True` on a ForeignKey has the same effect as using a OneToOneField."

## User Scenarios & Testing *(mandatory)*

**Note**: This is a data model correction with no user-facing changes. The goal is to eliminate a system warning by using the semantically correct field type (`OneToOneField`) in place of `ForeignKey(unique=True)`.

### User Story 1 - No System Warnings on Startup (Priority: P1)

As a system administrator, when I start the application server, I want no Django system check warnings related to the `PaymentReservation` model, so that the server output is clean and no misleading field type is used.

**Why this priority**: System warnings indicate an anti-pattern that should be corrected. The current `ForeignKey(unique=True)` is semantically equivalent to `OneToOneField` but uses the wrong field type.

**Independent Test**: Run `python manage.py check` and verify zero warnings related to `PaymentReservation.reservation`.

**Acceptance Scenarios**:

1. **Given** the application code is updated, **When** `python manage.py check` runs, **Then** the `fields.W342` warning about `PaymentReservation.reservation` is no longer present.
2. **Given** the field type is changed to `OneToOneField`, **When** a database migration runs, **Then** the migration applies cleanly without data loss or errors.
3. **Given** the updated model, **When** existing payment-reservation relationships are accessed, **Then** all relationships behave identically to before (read, write, cascade delete).

---

### Edge Cases

- What happens to the existing `ForeignKey` index on `reservation`? The `OneToOneField` includes an implicit unique constraint, so the existing index must be preserved or recreated in the migration as a unique constraint.
- What happens to reverse access via `Reservation.payment_links`? Since `OneToOneField` implies a single related object, `related_name` access would return a single object instead of a queryset. This must be verified — if any code iterates over `reservation.payment_links`, it must be updated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `PaymentReservation.reservation` field MUST use `models.OneToOneField` instead of `models.ForeignKey(unique=True)`.
- **FR-002**: A database migration MUST be generated that reflects the field type change without data loss.
- **FR-003**: Running `python manage.py check` MUST produce zero `fields.W342` warnings related to `PaymentReservation`.
- **FR-004**: All existing tests MUST pass after the change.
- **FR-005**: All user-visible strings MUST remain internationalized per Constitution Principle III.

### Key Entities

- **PaymentReservation**: A join record linking a `Payment` to a `Reservation` with a one-to-one constraint (each reservation belongs to at most one payment).
- **Payment**: The payment record (unchanged).
- **Reservation**: The reservation record (unchanged).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero `fields.W342` warnings when running `python manage.py check`.
- **SC-002**: All existing tests pass with no failures.
- **SC-003**: The database migration applies cleanly to both fresh databases and existing databases with data.
- **SC-004**: Payment-reservation associations function correctly: a reservation can be linked to a payment, and cascade delete works when the payment is removed.

## Assumptions

- The business rule that "each reservation has at most one payment" is correct and intentional.
- The change from `ForeignKey(unique=True)` to `OneToOneField` is purely a field-type substitution; no additional business logic changes are needed.
- The existing test suite provides adequate regression coverage for payment-reservation relationships.
- The `related_name="payment_links"` on a `OneToOneField` may change reverse-access semantics (queryset vs. single object). This must be handled as part of the implementation if any code relies on it.

## Out of Scope

- No changes to the `Payment` or `Reservation` models.
- No changes to payment creation, editing, or deletion workflows.
- No changes to templates, views, or URLs.
