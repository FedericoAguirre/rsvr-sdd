# Research: Translate Remaining Tags into Spanish

## Findings

### Target Strings

Four untranslated English strings found in `backend/apps/clients/templates/clients/_search_results.html`:

| String | Line | Context | Type |
|--------|------|---------|------|
| `"First"` | 46 | Pagination: first page link | `{% translate "First" %}` |
| `"Previous"` | 47 | Pagination: previous page link | `{% translate "Previous" %}` |
| `"Created"` | 22 | Table column header | `<th>{% translate "Created" %}</th>` |
| `"Yes,No"` | 31 | Active status display | `yesno:_("Yes,No")` |

### PO File Status

Checked `backend/locale/es/LC_MESSAGES/django.po` (335 lines). None of the 4 strings have entries. Related existing entries:

- `msgid "First name"` → `msgstr "Nombre"` (different from "First")
- `msgid "Created at"` → `msgstr "Creado en"` (different from "Created")
- `msgid "Yes,No"` → not present
- `msgid "Previous"` → not present

### Translation Consistency

Existing pagination translations from feature 011:
- `msgid "Next"` → `msgstr "Siguiente"`
- `msgid "Last"` → `msgstr "Último"`

New translations should follow the same pagination pattern.

### i18n Infrastructure

Project has Django i18n fully configured (LocaleMiddleware, LANGUAGE_CODE="es", LOCALE_PATHS set). No configuration changes needed.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Translation for "First" | `Primero` | Consistent with Spanish pagination conventions |
| Translation for "Previous" | `Anterior` | Consistent with Spanish pagination conventions |
| Translation for "Created" | `Creado` | Column header; differs from existing "Created at" → "Creado en" |
| Translation for "Yes,No" | `Sí,No` | Django `yesno` filter treats this as a single string |

## Alternatives Considered

- Using `makemessages` to auto-extract strings: simplest approach, run `django-admin makemessages -l es` and fill in msgstr values.
