# Implementation Plan: Add ClassPrice Sub-Option Under "Horario" Menu

**Branch**: `061-add-classprice-menu` | **Date**: 2026-08-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/061-add-classprice-menu/spec.md`

## Summary

Convert the "Horario" navigation item from a single flat link to a Bootstrap dropdown with two options: "Horario de Clases" (existing schedule page) and "Precios" (class price management page). This is a template-only change following the existing "Reportes" dropdown pattern.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Django 5.0.x, Bootstrap 5.3 (via CDN)

**Storage**: N/A (no model or migration changes)

**Testing**: pytest 9.1.x with pytest-django

**Target Platform**: Web browser (desktop + mobile responsive)

**Project Type**: Web application (Django backend with server-rendered templates)

**Performance Goals**: N/A (template change only, no performance impact)

**Constraints**: Must match existing "Reportes" dropdown pattern exactly (same Bootstrap classes, same HTML structure)

**Scale/Scope**: Single template file change (`backend/templates/base.html`); ~10 lines of HTML modified

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No constitution file exists at `.specify/memory/constitution.md`. Proceeding without constitution gates.

## Project Structure

### Documentation (this feature)

```text
specs/061-add-classprice-menu/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── templates/
│   └── base.html              # Nav menu change (line 28: flat link → dropdown)
├── apps/
│   └── classes/
│       ├── urls.py             # Unchanged (price-list URL already exists)
│       ├── views.py            # Unchanged
│       └── templates/classes/  # Unchanged
└── locale/es/LC_MESSAGES/      # Unchanged (translations already exist)
```

**Structure Decision**: Single file change in `backend/templates/base.html`. No view, URL, model, or migration changes needed.

## Complexity Tracking

No violations. No complexity added.
