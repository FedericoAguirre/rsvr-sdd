# Data Model: RSVR Sales Demonstration Script

**Date**: 2026-08-01
**Spec**: `specs/057-sales-demonstration-script/spec.md`

## Purpose

The feature introduces **no changes to the application data model**. This artifact documents the *logical structure* of the deliverable document and the *source domain entities* that the sales script references, so that implementation and validation stay grounded in the actual application.

## Deliverable Logical Structure (`docs/sales_script.md`)

The document is organized per the contract (`contracts/sales-script-contract.md`). Its internal "entities" are sections:

| Section | Logical Entity | Purpose |
|---------|----------------|---------|
| 1 | Purpose and Audience | Who the script serves and how to use it |
| 2 | Demonstration Preparation | Preconditions, demo data, account setup |
| 3 | Recommended Demonstration Flow | Ordered demo: overview → auth → nav → core workflow → data mgmt → reporting → admin |
| 4 | Feature Catalog | Lookup table of implemented features |
| 5 | Business Rules | Per-feature rules derived from app implementation |
| 6 | Feature Status and Known Gaps | Classification + gaps/future features |
| 7 | FAQ | Likely demonstration questions with answers |
| 8 | New Feature Request Questionnaire | 12-question capture form |
| 9 | Feature Request Handoff | Spec-Kit-ready template |
| 10 | Maintenance and Verification | How to keep the script current |

## Referenced Domain Entities (read-only, from app models)

These application models are the source of truth for feature/business-rule content. They are **not** modified.

- **Client** (`apps.clients.models.Client`): first_name, last_name, email (unique, nullable), mobile (unique, nullable), is_active. Rule: at least one of email/mobile required.
- **Reservation** (`apps.reservations.models.Reservation`): client FK, equipment FK (PROTECT), class_slot FK (PROTECT), date, status (reserved/used/unused), notes, created_by/updated_by. Rule: unique (equipment, class_slot, date).
- **ClassSlot** (`apps.classes.models.ClassSlot`): day_of_week (Mon–Fri), time (17:30/18:30), is_active. Rule: unique (day, time); inactive slots unavailable.
- **Equipment** (`apps.equipment.models.Equipment`): name, equipment_type (climber/treadmill/bike/elliptical/rower/other), status (in-service/out-of-service), notes.
- **Payment** (`apps.payments.models.Payment`): client FK (PROTECT), amount, payment_type (CASH/CC/DC/TRANSF/PAPP), payment_identifier (unique), date, class_slot_count, reference, evidence (image), notes, is_deleted/deleted_at (soft delete), created_by/updated_by.
- **PaymentReservation** (`apps.payments.models.PaymentReservation`): explicit link between Payment and Reservation; basis for the associated/unassociated reservation semantics in client payment history.

## Validation Rules Referenced

| Rule | Source | Impact on Sales Script |
|------|--------|------------------------|
| Client requires email or mobile | `Client.clean` | Documented as client creation rule |
| Duplicate reservation blocked | `unique_together (equipment, class_slot, date)` | Documented as duplicate-prevention rule |
| Equipment/ClassSlot protected from deletion while referenced | `PROTECT` | Documented limitation: must resolve reservations first |
| Payment identifier unique | `unique=True` | Documented as payment creation rule |
| Payments soft-deleted | `is_deleted`/`deleted_at` | Documented as record-lifecycle rule |
| Reports restricted to superusers | `UserPassesTestMixin` | Documented role/access rule |

## State Transitions

- **Reservation status**: `reserved → used` | `reserved → unused` (via status-change view). No transition back from used/unused.
- **ClassSlot**: `active ↔ inactive` via toggle (inactive hides from reservation creation).
- **Equipment**: `in-service ↔ out-of-service` via edit form.

## Relationships (summary)

```
Client 1──* Reservation *──1 ClassSlot
Client 1──* Payment
Reservation *──* Payment  (via PaymentReservation)
Equipment 1──* Reservation
```

No new relationships are introduced by this feature.
