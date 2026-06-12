# Data Model: Spanish Labels Translation

## Entities

### Translation Entry (within `.po` file)

| Attribute | Type | Description |
|-----------|------|-------------|
| msgid | str | English source string — the original text as it appears in code/templates |
| msgstr | str | Spanish translation — the translated text to display |
| msgctxt | str, optional | Disambiguation context (used when same English string has different Spanish translations depending on context) |
| msgid_plural | str, optional | English plural form (for pluralization support) |
| msgstr[0] | str | Singular Spanish translation (for pluralization) |
| msgstr[1] | str | Plural Spanish translation (for pluralization) |

**Note**: Translation entries are stored in `locale/es/LC_MESSAGES/django.po` as structured text, not in a database. This is a static artifact managed via Django's `makemessages` / `compilemessages` commands.

### Language Configuration (in Django settings)

| Setting | Value | Description |
|---------|-------|-------------|
| LANGUAGE_CODE | `'es'` | Default locale for the application |
| LANGUAGES | `[('en', 'English'), ('es', 'Español')]` | Available languages |
| LOCALE_PATHS | `[BASE_DIR / 'locale']` | Directory for `.po`/`.mo` files |
| USE_I18N | `True` | Enable i18n system (already set) |
| USE_L10N | `True` | Enable locale-aware formatting |

### Middleware Stack Addition

| Middleware | Purpose |
|------------|---------|
| `django.middleware.locale.LocaleMiddleware` | Activates the correct locale per request based on LANGUAGE_CODE and headers |

## Existing Data — No Schema Changes

This feature introduces **no database schema changes**. All translation data is stored in filesystem-based `.po`/`.mo` files under `backend/locale/`. The existing PostgreSQL schema (Client, Equipment, ClassSlot, Reservation models) remains unchanged.

## Validation Rules

1. Every `msgid` must have a non-empty `msgstr` (no untranslated strings)
2. `makemessages` must be run without errors (no syntax issues in templates/Python)
3. `compilemessages` must produce valid `.mo` files (no `msgfmt` errors)
4. No duplicate `msgid` entries across the entire `.po` file
5. HTML templates containing translation tags must all have `{% load i18n %}` at the top
