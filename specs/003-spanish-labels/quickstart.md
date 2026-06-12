# Quickstart: Translating Labels to Spanish

## Prerequisites

- GNU gettext installed (`brew install gettext` on macOS; `apt-get install gettext` on Linux)
- Docker Compose available (for running the app)

## Setup Translations

```bash
# 1. Enter the backend directory
cd backend

# 2. Extract all translatable strings from Python and templates
#    This scans all .py and .html files, generates/updates django.po
python manage.py makemessages --all

# 3. Edit the generated .po file at locale/es/LC_MESSAGES/django.po
#    Fill in the Spanish translations for each msgid

# 4. Compile translations to .mo format
python manage.py compilemessages

# 5. (If running in Docker) Compile inside the container
docker compose exec web python manage.py compilemessages
```

## Workflow for Adding New Strings

1. Add the English string in your code using `_()` / `{% translate %}` / `{% blocktrans %}`
2. Run `python manage.py makemessages --all` to extract new strings
3. Edit `locale/es/LC_MESSAGES/django.po` and add the Spanish translation
4. Run `python manage.py compilemessages`
5. Verify the new string renders in Spanish in the browser

## Testing Translations

```bash
# Run pytest — verify all pages render expected Spanish text
docker compose exec web python -m pytest

# Recompile messages if translations are not updating
docker compose exec web python manage.py compilemessages --force

# Verify no untranslated strings
python manage.py makemessages --all  # check for fuzzy/empty translations
```

## Django Settings to Enable

The following settings must be present in `backend/config/settings.py`:

```python
USE_I18N = True                          # Already set
USE_L10N = True                          # Enable locale-aware formatting
LANGUAGE_CODE = 'es'                     # Default to Spanish

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE.insert(                        # Insert after CommonMiddleware
    MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
    'django.middleware.locale.LocaleMiddleware',
)
```

## Notes

- **Committed artifacts**: Both `.po` (source) and `.mo` (compiled) files are committed to version control. This ensures translations work in CI/CD without installing gettext at deploy time.
- **Code stays English**: Only user-facing strings marked with `_()` / `{% translate %}` are extracted. Variable names, function names, comments, and docstrings remain in English.
- **Django admin**: Not translated as part of this feature — uses Django's built-in admin translations where available.
- **Date format**: With `USE_L10N = True` and `LANGUAGE_CODE = 'es'`, dates automatically display in dd/mm/yyyy format.
