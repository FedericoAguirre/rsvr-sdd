# Quickstart: Reports Menu Option

## What You're Building

Add a "Reports" dropdown to the main navigation bar with a "Payments" sub-item that links to `/payments/reports/`, visible only to admin users.

## Files to Change

1. **`backend/templates/base.html`** — Add Bootstrap dropdown markup for Reports > Payments, gated behind `{% if user.is_superuser %}`
2. **`backend/locale/es/LC_MESSAGES/django.po`** — Add translations for "Reports" and "Payments"

## Files to Create

1. **Test file** (in `backend/tests/` or existing app test) — Verify Reports menu visibility for admin vs non-admin users using `assertContains`

## Implementation Steps

1. Write and review tests (TDD)
2. Add Reports > Payments dropdown to navbar in `base.html`
3. Register i18n translations
4. Run tests
5. Run linting
6. Create PR

## Verification

```bash
# Run tests
cd backend && python manage.py test -v 2

# Compile translations
cd backend && django-admin compilemessages

# Run lint
cd backend && ruff check .
```
