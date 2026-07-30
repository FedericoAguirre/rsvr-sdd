# Research: Compact Payment Form Layout

**Feature**: 055-compact-payment-form
**Date**: 2026-07-30

## Bootstrap 5.3 Form Spacing & Utilities

**Decision**: Use Bootstrap 5.3 margin utilities (`mb-2`, `mb-3`, `g-2`) and form-control sizing (`form-control-sm`, `btn-sm`) for compact layout.

**Rationale**:
- Bootstrap 5.3 provides a comprehensive set of spacing utilities (`mb-0` through `mb-5`) that can be mixed and matched. Reducing `mb-4` to `mb-2` and `mb-3` to `mb-2` saves ~18–48px of vertical space.
- Form grid gutters (`g-2`, `g-3`) control column spacing and are fully responsive.
- `form-control-sm` and `btn-sm` classes reduce input/button heights without custom CSS.
- Fieldset legends are stripped of borders and padding by default in Bootstrap 5.3's Reboot, making them suitable as section headers with custom styling.

**Alternatives considered**:
- Custom CSS overriding all Bootstrap defaults: rejected — fragile, harder to maintain.
- Third-party compact form library: rejected — unnecessary dependency.

## CSS-Only Help Text Toggle

**Decision**: Use CSS sibling selector (`.form-control:focus ~ .form-help-collapsed`) with `display: none`/`display: block` toggle, supplemented by JavaScript for blur removal.

**Rationale**:
- CSS-only approach works for initial display on focus but cannot hide help text on blur when field value exists.
- JavaScript is needed for `blur` to hide help text if empty, keep visible if value present.
- Semantically, help text is associated with the field via `.form-text` class and `data-field` attribute.

**Alternatives considered**:
- Always-visible help text: rejected — adds ~60-80px of vertical space.
- Tooltip on hover only: rejected — not accessible via keyboard navigation.

## Current Template Analysis

**Template path**: `backend/apps/payments/templates/payments/payment_form.html`

**Current spacing**:
| Element | Current | Compact target | Saving |
|---------|---------|---------------|--------|
| Page title | `h2.mb-4` | `h4.mb-2` | ~20px |
| Fieldset margins | `mb-4` (×3) | `mb-2` (×3) | ~48px |
| Field margins | `mb-3` (×9) | `mb-2` (×9) | ~18px |
| Label font | `1rem` | `0.9rem` | ~5px |
| Legend font | Default | `0.875rem` | ~5px |
| Form control padding | `0.5rem` | `0.375rem` | ~8px |
| Fieldset padding | `1rem` | `0.75rem` | ~8px |
| Help text display | Always visible | Hidden by default | ~60px |
| Button spacing | `2rem` margin | `1rem` margin | ~16px |

**Estimated total saving**: ~188px (25% reduction)

## Accessibility Considerations

**Decision**: Maintain WCAG AA compliance with compact layout.

- Help text uses `.form-text` class (semantic association) and `data-field` attribute for JS targeting.
- Focus states remain visible — Bootstrap's default `:focus-visible` ring is preserved.
- Error messages use Bootstrap's `.text-danger` and Django's error rendering unchanged.
- Labels are explicitly associated with inputs via Django form rendering (`.as_p` or explicit `<label>` tags).
- Touch targets on mobile: maintain minimum 44×44px per WCAG 2.2.

## Django i18n

**Decision**: All existing i18n strings are preserved. No new user-visible strings are introduced by the compact layout changes (labels, help text, and button text remain the same).
