# Quickstart: Translate English Tags into Spanish

## What needs to be done

Add 8 English→Spanish translation entries to the project's i18n system and fix a missing model attribute.

## Files to modify

### 1. Equipment model — Add singular `verbose_name`

**File**: `backend/apps/equipment/models.py` (line ~28)

Add to the `Equipment.Meta` class:
```python
class Meta:
    ordering = ["name"]
    verbose_name = _("Equipment")       # ← ADD THIS
    verbose_name_plural = _("equipment") # ← already exists
```

### 2. Django PO file — Add 8 translation entries

**File**: `backend/locale/es/LC_MESSAGES/django.po`

Add these entries:

```po
#: apps/clients/templates/clients/search.html:17
msgid "Searching..."
msgstr "Búsqueda..."

#: apps/clients/forms.py:11
msgid "Search clients..."
msgstr "Buscar clientes..."

#: apps/clients/templates/clients/_search_results.html:7
#, python-format
msgid "Filtered by \"%(q)s\""
msgstr "Filtrado por \"%(q)s\""

#: apps/clients/templates/clients/_search_results.html:12
msgid "Client NOT FOUND"
msgstr "Cliente NO ENCONTRADO"

#: apps/clients/templates/clients/_search_results.html:62
msgid "Start typing to search clients..."
msgstr "Empiece a escribir para buscar clientes..."

#: apps/clients/templates/clients/_search_results.html:55
msgid "Next"
msgstr "Siguiente"

#: apps/clients/templates/clients/_search_results.html:56
msgid "Last"
msgstr "Último"

#: apps/equipment/models.py:28
msgid "Equipment"
msgstr "Equipo"
```

### 3. Update existing PO entry for "Equipment"

**File**: `backend/locale/es/LC_MESSAGES/django.po`

Change the existing entry (around line 103-104):
```po
# Before:
msgid "Equipment"
msgstr "Equipos"

# After:
msgid "Equipment"
msgstr "Equipo"
```

### 4. Compile translations

```bash
cd backend
uv run django-admin compilemessages
```

This regenerates `backend/locale/es/LC_MESSAGES/django.mo`.

## How to verify

1. Navigate to `clients/search/` — confirm all text is in Spanish
2. Navigate to `admin/equipment/equipment/` — confirm "Seleccione equipo a modificar" and "AÑADIR EQUIPO" are displayed
3. Run `django-admin compilemessages` — confirm no errors
4. Run tests — confirm no regressions

## How to generate PO entries automatically (alternative)

```bash
cd backend
uv run django-admin makemessages -l es
```

This scans all templates and Python files for translatable strings and adds them to `django.po`. Then fill in the `msgstr` values manually.
