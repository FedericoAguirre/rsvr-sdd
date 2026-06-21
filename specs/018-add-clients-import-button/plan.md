# Implementation Plan: Add Clients Import Button

**Branch**: `018-add-clients-import-button` | **Date**: 2026-06-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/018-add-clients-import-button/spec.md`

## Summary

Replace the "Búsqueda..." placeholder/legend on `/clients/search/` with a "Subir Clientes" navigation element that links to `/clients/upload/`. This is a frontend-only change — the upload page already exists from feature `016-csv-client-upload`. The change involves modifying the `search.html` template and adding/updating i18n translation strings.

## Technical Context

**Language/Version**: Python 3.12+ / Django 5.0.x

**Primary Dependencies**: Django templates, Bootstrap 5.3.3, HTMX 2.0.4

**Storage**: N/A (no new data)

**Testing**: pytest 9.1+ / pytest-django 4.12+

**Target Platform**: Web (Linux/macOS via Docker Compose)

**Project Type**: Web application (Django)

**Performance Goals**: N/A (navigation-only change, no measurable performance impact)

**Constraints**: Must use existing i18n patterns (`{% translate %}` / `{% blocktranslate %}`), must follow existing template conventions (Bootstrap classes, HTMX not required for this element)

**Scale/Scope**: Single template change, single route addition (clients/search/ already exists)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: TDD Compliance (NON-NEGOTIABLE)

- **Requirement**: Tests MUST be written by the user first, MUST fail before implementation. Integration tests required for contract changes.
- **Assessment**: This feature introduces a new navigation element on an existing page. The change touches a template and potentially the form/widget. Tests must verify:
  - The "Subir Clientes" element is present on `/clients/search/`
  - Clicking it navigates to `/clients/upload/`
  - The element uses the correct Spanish text (i18n)
- **Verdict**: PASS — tests can be written first as described above.

### Gate 2: UX Consistency

- **Requirement**: All user-facing interfaces MUST use i18n. New text MUST be translated to Spanish.
- **Assessment**: "Subir Clientes" is already Spanish, but it must use Django's `{% translate %}` tag with a corresponding `msgid` in `django.po` for consistency.
- **Verdict**: PASS — follow existing i18n patterns.

### Gate 3: Code Quality

- **Requirement**: No dead code, YAGNI, pass linting, code review required.
- **Assessment**: Minimal change — replace/add a single element. No complexity concern.
- **Verdict**: PASS.

### Gate 4: Performance

- **Requirement**: Define measurable performance criteria before implementation.
- **Assessment**: Navigation-only change, no measurable performance criteria needed.
- **Verdict**: PASS — N/A for this feature scope.

## Project Structure

### Documentation (this feature)

```text
specs/018-add-clients-import-button/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A — no new entities)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
# Web application (Django)
backend/
├── apps/
│   └── clients/
│       ├── templates/clients/
│       │   └── search.html      # [MODIFY] Replace "Búsqueda..." with "Subir Clientes" element
│       ├── forms.py              # [MODIFY] Update placeholder text
│       └── urls.py               # (no change — /upload/ already exists)
├── locale/es/LC_MESSAGES/
│   ├── django.po                # [MODIFY] Add/update translation strings
│   └── django.mo                # [REBUILD] Compile translations
└── tests/
    ├── test_client_list.py      # (no change)
    ├── test_client_csv_upload.py # (no change)
    └── test_i18n.py             # [MODIFY] Add test for "Subir Clientes" label
```

**Structure Decision**: Single Django project. The change is confined to the `clients` app's template and forms. No new files needed.

## Complexity Tracking

N/A — No constitution violations. Change is trivial (single element replacement).
