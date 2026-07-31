# Contracts: Compact Payment Form Layout

## UI Contract

The payment form template (`payment_form.html`) is the single interface contract for this feature. It defines:

1. **HTML structure**: The three-fieldset layout (Transaction Data, Context, Documentation and Reference) with responsive grid classes.
2. **CSS classes**: Bootstrap 5.3 utility classes and custom compact classes (`.form-label-compact`, `.form-help-collapsed`, `.payment-form-container`, `.form-actions`).
3. **Behavior**: Help text visibility toggles on field focus/hover; error messages display below fields; action buttons at form bottom.
4. **Responsive breakpoints**: Desktop multi-column (>= 1024px), tablet adjusted (769–1024px), mobile stacked (< 768px).

### Contract Invariants (Must Not Change)

- All form fields from `PaymentForm` must be rendered (no fields removed).
- Form submission, validation, and file upload behavior must be preserved.
- The `{% csrf_token %}` must be present.
- Buttons must be fully visible and functional.
- All labels must use i18n translation (no hardcoded strings).

### Responsive Behavior Matrix

| Viewport | Columns per Row | Button Layout | Help Text |
|----------|----------------|---------------|-----------|
| Desktop >= 1024px | Multi-column (col-md-4/6) | Horizontal, side-by-side | Hidden, shows on focus |
| Tablet 769–1024px | Multi-column, tighter gaps | Horizontal, side-by-side | Hidden, shows on focus |
| Mobile < 768px | Full-width stacked | Full-width stacked, vertical | Hidden, shows on focus |
