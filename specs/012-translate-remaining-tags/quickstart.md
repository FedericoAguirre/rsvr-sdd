# Quickstart: Translate Remaining Tags into Spanish

## What to do

Add 4 entries to `backend/locale/es/LC_MESSAGES/django.po`:

```po
#: apps/clients/templates/clients/_search_results.html:22
msgid "Created"
msgstr "Creado"

#: apps/clients/templates/clients/_search_results.html:31
msgid "Yes,No"
msgstr "Sí,No"

#: apps/clients/templates/clients/_search_results.html:46
msgid "First"
msgstr "Primero"

#: apps/clients/templates/clients/_search_results.html:47
msgid "Previous"
msgstr "Anterior"
```

## Compile

```bash
cd backend
uv run django-admin compilemessages
```

## Verify

1. Navigate to clients/search — confirm pagination shows "Primero" and "Anterior"
2. Confirm table header shows "Creado" instead of "Created"
3. Confirm active clients show "Sí" instead of "Yes"
4. Run tests: `uv run pytest`
