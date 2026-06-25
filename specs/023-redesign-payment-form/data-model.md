# Data Model: Payment Form Redesign

**Date**: 2026-06-24

## Status

No data model changes required. This feature is purely a UI/UX redesign of the existing payment form template and form class.

### Payment Model (existing)

The `Payment` model at `apps/payments/models.py` is unchanged. For reference, its fields are:

| Field | Type | Purpose |
|---|---|---|
| client | ForeignKey → Client | Payment belongs to one client |
| amount | DecimalField | Payment amount |
| payment_type | CharField (choices) | CC, CASH, DEBIT, TRANSFER, PAYAPP |
| payment_identifier | CharField | Auto-generated unique ID |
| date | DateField | Payment date |
| class_slot_count | IntegerField | How many class slots this covers |
| reference | CharField (optional) | External reference |
| evidence | ImageField (optional) | Proof of payment |
| notes | TextField (optional) | Operator notes |
| created_by | ForeignKey → User | Who created the payment |
| created_at | DateTimeField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated |
| updated_by | ForeignKey → User (nullable) | Who last modified |
| is_deleted | BooleanField | Soft-delete flag |

### Form class (to be modified)

`PaymentForm` at `apps/payments/forms.py` — ModelForm for the Payment model. Changes:
- All widget attrs in `Meta.widgets` gain `"class": "form-control"`
- New widget entries for fields without explicit widgets (`client`, `amount`, `payment_type`, `payment_identifier`, `class_slot_count`, `reference`, `evidence`)

### Template (to be modified)

`templates/payments/payment_form.html` — the form template. Changes:
- Field wrapper `<div class="col-12">` → `<div class="col-md-6">`
- Button row remains `<div class="col-12">`
