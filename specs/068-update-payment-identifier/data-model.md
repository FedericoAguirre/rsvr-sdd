# Data Model: Payment Receipt Identifier Integration

## Existing Entities

### Payment

The selected financial transaction.

| Field | Source | Role in this change | Rules |
|---|---|---|---|
| `payment_identifier` | `Payment.payment_identifier` | Public identifier shown in PDF/Markdown and used in the PDF filename | Unique, required by normal model save behavior, human-readable, max 50 characters |
| `reference` | `Payment.reference` | Legacy internal/reference value | May be blank or null; no longer used as the public receipt identifier or PDF filename component |
| `client` | `Payment.client` | Related client used in receipt and filename | Existing protected foreign-key relationship |
| `amount` | `Payment.amount` | Receipt header value | Existing formatting preserved |
| `payment_type` | `Payment.payment_type` | Localized receipt header value | Existing display choice preserved |
| `date` | `Payment.date` | Receipt header and reservation date context | Existing active-language formatting preserved |
| `class_slot_count` | `Payment.class_slot_count` | Receipt header value | Existing value preserved |

### Client

The client associated with the payment. Its first and last names form the filename client component, which is sanitized before use.

### Payment Reservation and Reservation

Existing linked records provide class slot, date, equipment, and status rows. Their relationship and ordering are unchanged by this feature.

## Derived Receipt Projection

`build_receipt(payment)` produces a non-persistent projection consumed by both output renderers.

| Projection member | Description |
|---|---|
| `labels` | Active-language labels, including a translated payment-identifier label |
| `client` | Display client name |
| `identifier` | String form of `payment.payment_identifier` |
| `amount`, `payment_type`, `date`, `class_slot_count` | Existing localized/formatted header values |
| `filename` | `payment_<sanitized-client>_<sanitized-identifier>.pdf` |
| `reservations` | Existing ordered reservation rows |

## Validation Rules

- The projection must source the public identifier from `payment.payment_identifier`, never from `payment.reference`.
- Receipt content must preserve the identifier’s readable characters, including accents where the renderer supports them.
- Filename client and identifier components must pass through the existing safe filename normalization before concatenation.
- Empty or unsafe filename components must resolve to the helper’s non-empty fallback and must not permit path separators or control characters.
- No database fields, relationships, state transitions, or migrations are introduced.
