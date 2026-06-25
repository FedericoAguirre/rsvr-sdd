# Contracts: Payment Form Redesign

**Date**: 2026-06-24

## Status

No contract changes. This feature modifies only:

- `backend/apps/payments/forms.py` — widget attrs (internal)
- `backend/apps/payments/templates/payments/payment_form.html` — CSS classes (internal)

### Unchanged Contracts

| Interface | Status | Notes |
|---|---|---|
| URL patterns (`/payments/create/`, `/payments/<pk>/edit/`) | Unchanged | No route changes |
| View signatures (PaymentCreateView, PaymentUpdateView) | Unchanged | No argument or return type changes |
| Payment model fields and validation | Unchanged | No schema changes |
| Form field names and types | Unchanged | No behavioral changes |
| i18n translation keys | Unchanged | No new or modified strings |
