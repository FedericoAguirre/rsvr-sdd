# Implementation Plan: Spanish Labels Translation

**Branch**: `003-labels-to-spanish` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-spanish-labels/spec.md`

## Summary

Translate all user-facing labels in the Django gym reservation web application from English to Spanish using Django's built-in i18n framework (`gettext`/`gettext_lazy`). Source code (Python, templates, variable names, comments) remains in English. The application currently has ~70+ hardcoded English strings across 12 HTML templates, 4 model files, 4 view files, 2 form files, and 1 management command. Django's `USE_I18N = True` is already set but never utilized — this feature wires up the full i18n pipeline.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Django i18n (`gettext` / `gettext_lazy`), `django-admin makemessages` / `compilemessages`, gettext toolchain (system-level `xgettext`)

**Storage**: PostgreSQL 16 — no schema changes needed

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker container)

**Project Type**: Web application (Django + Bootstrap/HTML5)

**Performance Goals**: Translation lookup should add <50ms per page load; no measurable regression from baseline

**Constraints**: All user-facing strings must use Django's i18n; source code (variable names, comments, docstrings) stays in English; `.po`/`.mo` files committed to repo

**Scale/Scope**: ~70+ user-facing strings across 12 templates + Python source; single target locale (es)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Evaluation

| Principle | Assessment | Status |
|-----------|-----------|--------|
| I. Code Quality | Standard Django i18n patterns (`{% load i18n %}`, `{% translate %}`, `_()`, `gettext_lazy`); ruff linting unaffected; no dead code | ✅ PASS |
| II. Testing Standards (NON-NEGOTIABLE) | TDD applies — acceptance tests for Spanish text on every page must be written before implementation; pytest verifies each page renders expected Spanish labels | ✅ PASS |
| III. User Experience Consistency | All translations defined upfront in spec; consistent Spanish terminology across all pages; date format follows Spanish locale | ✅ PASS |
| IV. Performance Requirements | Translation overhead <50ms per page; no measurable impact on existing response times | ✅ PASS |

**Result**: All gates pass. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/003-spanish-labels/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   ├── clients/         # Add {% load i18n %}, translate labels in templates/forms/models
│   ├── equipment/       # Add {% load i18n %}, translate labels in templates/forms/models
│   ├── classes/         # Add {% load i18n %}, translate labels in templates/models
│   └── reservations/    # Add {% load i18n %}, translate labels in templates/models
├── templates/           # Translate base.html and login.html
│   ├── base.html
│   └── registration/
├── locale/              # NEW — Django locale directory
│   └── es/
│       └── LC_MESSAGES/
│           ├── django.po     # All translations
│           └── django.mo     # Compiled translations
├── config/
│   └── settings.py      # Enable LocaleMiddleware, LANGUAGES, LOCALE_PATHS
└── manage.py
```

**Structure Decision**: Standard Django i18n project layout. The `locale/` directory is added at the Django project root level (not per-app), following the single-source-of-truth pattern. All translations are collected into one `.po` file per language via `django-admin makemessages --all`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations — standard Django i18n patterns throughout.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
