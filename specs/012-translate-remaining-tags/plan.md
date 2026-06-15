# Implementation Plan: Translate Remaining Tags into Spanish

**Branch**: `012-translate-remaining-tags` | **Date**: 2026-06-15 | **Spec**: `specs/012-translate-remaining-tags/spec.md`

**Input**: Feature specification from `specs/012-translate-remaining-tags/spec.md`

## Summary

Add 4 Spanish translation entries to `django.po` for remaining English strings in clients/search: "First" → "Primero", "Previous" → "Anterior", "Created" → "Creado", "Yes,No" → "Sí,No".

## Technical Context

**Language/Version**: Python 3.x / Django 5.x

**Primary Dependencies**: Django i18n (built-in `django.utils.translation`)

**Storage**: N/A — translations stored in `.po`/`.mo` files at `backend/locale/es/LC_MESSAGES/`

**Testing**: pytest (existing project test suite)

**Target Platform**: Web server

**Project Type**: Web application (Django)

**Performance Goals**: N/A — text localization only

**Constraints**: N/A

**Scale/Scope**: 4 translation entries, 1 file to modify

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gates

| Gate | Status | Justification |
|------|--------|---------------|
| **I. Code Quality** | ✅ PASS | Only adding PO entries; no code quality concerns |
| **II. Testing Standards (NON-NEGOTIABLE)** | ✅ PASS | Translations verifiable by page content inspection |
| **III. User Experience Consistency** | ✅ PASS | Completes Spanish localization for clients/search |
| **IV. Performance Requirements** | ✅ PASS | Zero performance impact |

**No violations. Complexity Tracking not required.**

## Project Structure

### Documentation

```text
specs/012-translate-remaining-tags/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # No external interfaces
└── tasks.md             # Created by /speckit.tasks
```

### Source Code

```text
backend/
├── locale/
│   └── es/
│       └── LC_MESSAGES/
│           └── django.po          # [MODIFY] Add 4 translation entries
└── apps/clients/templates/clients/
    └── _search_results.html        # [NO CHANGE] Already uses {% translate %}
```
