# Data Model: Price Format Display

**Feature**: 063-price-format
**Date**: 2026-08-02

## Summary

No data model changes are required for this feature. The `ClassPrice` model's `price` field (`DecimalField(max_digits=10, decimal_places=2)`) stores the correct value. Formatting is applied exclusively at the presentation layer via the `currency` template filter.

## Existing Entity: ClassPrice

**Source**: `backend/apps/classes/models.py`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `price` | `DecimalField(10, 2)` | Required | Raw monetary value. Display formatted as `$N,NNN.NN` via template filter. |
| `current` | `BooleanField` | `default=True` | Flags the active/current price. |
| `created_by` | `FK → User` | `PROTECT` | User who created the price record. |
| `created_at` | `DateTimeField` | `auto_now_add` | When the record was created. |
| `changed_at` | `DateTimeField` | `null=True` | When this price was superseded. |
| `changed_by` | `FK → User` | `null=True, PROTECT` | User who superseded this price. |
| `updated_at` | `DateTimeField` | `auto_now` | Last modification timestamp. |

No new entities, fields, relationships, or migrations are introduced.

## Validation

Existing validation in `backend/apps/classes/forms.py` (line 23-28) remains unchanged:

```python
def clean_price(self):
    price = self.cleaned_data.get("price")
    if price is not None and Decimal(price) <= 0:
        raise ValidationError(_("Enter a positive amount."))
    return price
```

## State Transitions

None. Display formatting does not affect entity state.
