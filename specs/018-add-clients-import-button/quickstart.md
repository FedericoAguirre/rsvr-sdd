# Quickstart: Add Clients Import Button

## Files to Modify

| File | Change |
|------|--------|
| `backend/apps/clients/templates/clients/search.html` | Add "Subir Clientes" link in the action button row |
| `backend/locale/es/LC_MESSAGES/django.po` | Add `msgid "Upload Clients"` / `msgstr "Subir Clientes"` entry |
| `backend/tests/test_i18n.py` | Add test for "Subir Clientes" label rendering |

## Commands

```bash
# Compile translations after editing django.po
django-admin compilemessages

# Run tests
python -m pytest backend/tests/

# Run specific tests
python -m pytest backend/tests/test_i18n.py -v
```

## Verification

1. Start the app: `make up` (Docker Compose)
2. Log in and navigate to `/clients/search/`
3. Verify "Subir Clientes" link is visible alongside the search form
4. Click it and verify navigation to `/clients/upload/`
