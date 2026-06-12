# Research: Spanish Labels Translation

## Technology Decisions

### Django i18n Framework

- **Decision**: Use `django.utils.translation` (`gettext` / `gettext_lazy`) for Python code and `{% load i18n %}` / `{% translate %}` / `{% blocktrans %}` for Django templates
- **Rationale**: Django's i18n is already partially configured (`USE_I18N = True` in settings). It provides a mature translation pipeline with string extraction (`makemessages`), compilation (`compilemessages`), and runtime lazy translation via `gettext_lazy` for model fields. No additional dependencies needed.
- **Alternatives considered**: Custom string mapping dict (no tooling, manual extraction); third-party packages like `django-rosetta` (overkill for single-language translation); replacing strings in-place (loses English source, hard to maintain)

### Gettext Toolchain

- **Decision**: Use GNU gettext utilities (xgettext, msgfmt) via Django management commands
- **Rationale**: Django's `makemessages` wraps xgettext for automatic string extraction. `compilemessages` wraps msgfmt for `.po` → `.mo` compilation. Both are standard Django workflow. Requires `gettext` system package in Docker image.
- **Alternatives considered**: Manual `.po` file editing without extraction (error-prone); custom extraction script (duplicates Django built-in)

### Translations as Code

- **Decision**: Commit `.po` and `.mo` files to version control
- **Rationale**: Translations are part of the application. Committing compiled `.mo` files ensures they are available in CI/CD and production without a compilation step. Standard practice for Django projects.
- **Alternatives considered**: Compile at deploy time (adds build step, risk of missing toolchain); store in external service (overkill for single-language)

### Locale Middleware

- **Decision**: Add `LocaleMiddleware` to `MIDDLEWARE` and configure `LANGUAGE_CODE = 'es'` as the default
- **Rationale**: `LocaleMiddleware` activates the correct locale based on `LANGUAGE_CODE` and the `Accept-Language` header. Setting `LANGUAGE_CODE = 'es'` makes Spanish the default without requiring URL prefix or session-based switching.
- **Alternatives considered**: URL prefix `/es/...` (adds route complexity); session-based (unnecessary for single-language app); cookie-based (same)

## Domain Research

### Django i18n Best Practices

- `gettext_lazy` should be used for strings in model fields (`verbose_name`, `help_text`), form labels, and choices — these are evaluated at import time, so lazy evaluation is required
- `gettext` (non-lazy) is appropriate for view messages and any string evaluated at runtime
- Template tags `{% translate %}` and `{% blocktrans %}` handle translation in templates; `{% blocktrans %}` is needed when the string contains template variables
- The `{% load i18n %}` tag must be added to every template that uses translation tags
- `makemessages` scans all Python files and templates under the project root; the `--extension` flag controls which file extensions are scanned
- The `.po` file format uses `msgid` (English source) and `msgstr` (Spanish translation). Plural forms are handled via `msgid_plural`

### Spanish Locale Conventions

- Date format: dd/mm/yyyy (day first)
- Time format: HH:MM (24-hour, same as English)
- Decimal separator: comma (not used in this app)
- Currency: not used in this app
- Day names: lunes, martes, miércoles, jueves, viernes
- No formal/informal pronoun distinction needed (staff tool, "usted" implied)

### Translation Patterns for Django Models

- Model `__str__` methods should use `gettext` or `gettext_lazy` with format strings: `_("{client} – {equipment} – {date}").format(...)`
- Choice fields should use `gettext_lazy` on each choice label, or apply translation in the template
- `verbose_name` and `verbose_name_plural` should use `gettext_lazy`

### Docker Integration

- GNU gettext is required in the Docker image for `compilemessages`
- `apt-get install gettext` should be added to Dockerfile if not present
- Alternative: pre-compile `.mo` files and commit them (avoids runtime dependency)
