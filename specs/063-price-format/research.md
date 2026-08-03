# Research: Price Format Display

**Feature**: 063-price-format
**Date**: 2026-08-02

## Decision 1: How to provide the `currency` filter to the classes app

### Decision
Load the existing `payment_extras` templatetag library directly in `class_prices.html`.

### Rationale
1. The `currency` filter in `backend/apps/payments/templatetags/payment_extras.py` already produces the exact format requested (`$N,NNN.NN` via `f"${float(value):,.2f}"`).
2. No shared/core templatetags module exists in the project; the convention is per-app `{appname}_extras.py`. Creating a new shared app for this would be over-engineering for a 6-line filter.
3. `apps.payments` is hardcoded in `INSTALLED_APPS` — it will never be conditionally removed, so cross-app loading is safe.
4. The change is minimal: add `payment_extras` to the `{% load %}` tag (1 line) and pipe `currency` filter on two template expressions.

### Alternatives Considered
- **Create a shared `apps/core` app**: Architecturally cleaner but introduces a new app, migrations, boilerplate, and requires updating 5 payment templates. Disproportionate for this feature.
- **Duplicate filter in `classes/templatetags/class_extras.py`**: DRY violation. Two copies to maintain.
- **Use `django.contrib.humanize` `intcomma` filter**: Doesn't add the `$` sign or two-decimal formatting. Would require chaining with `floatformat` and a currency prefix, producing inconsistent output.

## Decision 2: Template locations to modify

### Decision
Two locations in `class_prices.html`: the "Current prices" alert (line ~17) and the history table cell (line ~40).

### Rationale
These are the only places where `{{ price.price }}` is rendered to the user. The form input field (`class_price_form.html`) uses a `NumberInput` widget and should remain unchanged — the form renders raw numeric values for browser-native validation.

## Decision 3: Testing approach

### Decision
Write Django `TestCase` tests that render `class_prices.html` with a known `ClassPrice` instance and assert the formatted output contains the expected string `$1,500.00` (or equivalent).

### Rationale
Constitution Principle II (Testing Standards) requires tests. Since this is a template-level change with no new logic, template rendering integration tests are the appropriate level.

## Decision 4: i18n impact

### Decision
No new i18n entries needed.

### Rationale
The `$` symbol is static formatting, not a user-visible string. The spec and Constitution Principle III (i18n) apply to "user-visible strings" (headers, labels, buttons, etc.) — numeric formatting is not in scope.
