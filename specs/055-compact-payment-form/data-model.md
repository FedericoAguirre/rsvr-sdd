# Data Model: Compact Payment Form Layout

**Feature**: 055-compact-payment-form

## No Data Model Changes

This feature does **not** introduce any changes to the application's data model. It is a purely presentational change affecting only the Django template (`payment_form.html`) and its embedded CSS.

## Affected Entities

### PaymentForm (Django Form, not Model)

The `PaymentForm` class in `backend/apps/payments/forms.py` is **not modified** — only its rendering template changes.

| Field | Display Column Width (Create Mode) | Display Column Width (Edit Mode) |
|-------|-----------------------------------|----------------------------------|
| client | `col-12` | N/A (loop) |
| amount | `col-md-6` | N/A (loop) |
| class_slot_count | `col-md-6` | N/A (loop) |
| payment_type | `col-12` | N/A (loop) |
| date | `col-md-6` | N/A (loop) |
| notes | `col-md-6` | N/A (loop) |
| payment_identifier | `col-md-4` | N/A (loop) |
| reference | `col-md-4` | N/A (loop) |
| evidence | `col-md-4` | N/A (loop) |

**Key difference from current (054) layout**: Documentation section changes from 2-column (payment_identifier + reference side-by-side, evidence full-width) to 3-column (all three side-by-side via `col-md-4`).

## Template Layout Structure

```text
.payment-form-container (max-width: 900px, centered)
├── h4.mb-2 (title)
└── form.payment-form
    ├── fieldset.mb-2 (Transaction Data)
    │   ├── div.mb-2 (client)
    │   ├── div.row.g-2
    │   │   ├── div.col-md-6.mb-2 (amount)
    │   │   └── div.col-md-6.mb-2 (class_slot_count)
    │   └── div.mb-2 (payment_type)
    ├── fieldset.mb-2 (Context)
    │   └── div.row.g-2
    │       ├── div.col-md-6.mb-2 (date)
    │       └── div.col-md-6.mb-2 (notes)
    ├── fieldset.mb-2 (Documentation and Reference)
    │   └── div.row.g-2
    │       ├── div.col-md-4.mb-2 (payment_identifier)
    │       ├── div.col-md-4.mb-2 (reference)
    │       └── div.col-md-4.mb-2 (evidence)
    └── div.form-actions
        ├── button.btn.btn-primary.btn-sm (submit)
        └── a.btn.btn-secondary.btn-sm (cancel)
```
