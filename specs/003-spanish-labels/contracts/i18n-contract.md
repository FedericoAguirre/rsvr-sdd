# i18n Contract: Spanish Labels Translation

## Translation Interface Contract

This feature does not introduce new public API endpoints, CLI commands, or external interfaces. It modifies the **presentation layer** of the existing Django web application.

### What Changes

All user-facing output (HTML templates, Django form labels, model verbose names, choice labels, success/error messages) gains a Spanish translation layer via Django's i18n system.

### Contract Guarantees

| Aspect | Before | After |
|--------|--------|-------|
| Template output | Hardcoded English | `{% load i18n %}` + `{% translate %}` — renders Spanish |
| HTML lang attribute | `lang="en"` | `lang="es"` |
| Date/time display | English/US format | Spanish locale (dd/mm/yyyy) |
| Python messages | Plain English strings | Wrapped in `_()` / `gettext()` / `gettext_lazy()` |
| Model `__str__` | English format strings | Wrapped in `gettext()` |
| Admin panel | English (Django defaults) | Unchanged (uses Django admin i18n) |

### What Does Not Change

- URL structure and routes
- HTTP method semantics
- Request/response status codes
- Form submission and validation behavior
- Database schema and data
- Authentication and authorization
- Python variable/function/class names
- Code comments and docstrings
- CSS, JavaScript (static files unchanged)

### Verification Contract

Tests must verify that every user-facing page renders expected Spanish text. The contract can be validated by:

1. Loading each page/template
2. Checking for the presence of Spanish label strings (as defined in spec acceptance scenarios)
3. Verifying no English source strings appear where translation is expected
4. Confirming `.mo` files compile without errors
5. Confirming that untranslated strings fall back to English gracefully
