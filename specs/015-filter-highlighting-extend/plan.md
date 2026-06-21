# Implementation Plan: Extend Filter Highlighting to Email and Mobile

**Branch**: `017-filter-highlighting-extend` | **Date**: 2026-06-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/015-filter-highlighting-extend/spec.md`

## Summary

Extend the existing name-search highlighting to email and mobile number columns in the clients search results. The existing `highlight` template tag already supports case-insensitive regex matching with `<mark>` tags. Mobile number matching will strip non-numeric characters before comparison.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Django 5.0, Bootstrap 5.3, HTMX (via django-htmx)

**Storage**: PostgreSQL 16

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker)

**Project Type**: Web application (Django server-rendered templates)

**Performance Goals**: <500ms page load, dynamic search via HTMX with 300ms debounce

**Constraints**: Server-rendered Django templates, no separate frontend framework. All UI changes in `.html` template files and Python `templatetag` files.

**Scale/Scope**: Internal gym management system, <1,000 client records

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment | Details |
|-----------|------------|---------|
| I. Code Quality | ✅ Pass | Linting (Ruff) enforced. No new complexity introduced. |
| II. Testing Standards | ✅ Pass | TDD applicable. Existing test pattern in `backend/tests/test_client_search_name.py` provides model. |
| III. UX Consistency | ✅ Pass | Highlighting extends existing visual treatment (mark tags). Any new UI strings must be i18n'd. |
| IV. Performance | ✅ Pass | No new queries — only template-level change on already-fetched data. |
| Technology Constraints | ✅ Pass | No new dependencies. |
| Development Workflow | ✅ Pass | Feature branch exists. |

**Gate verdict**: Pass — no constitutional violations.

## Project Structure

### Documentation (this feature)

```text
specs/015-filter-highlighting-extend/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── clients/
│       ├── templatetags/
│       │   └── client_extras.py      # highlight filter — add mobile normalization
│       └── templates/
│           └── clients/
│               └── _search_results.html  # add |highlight:q to email and mobile cells
└── tests/
    └── test_client_search_highlighting.py  # new test file

ai/
└── sessions/       # compressed session files per constitution
```

**Structure Decision**: Existing Django app structure — no structural changes needed. Feature is limited to template tag logic and template updates.

## Complexity Tracking

> No complexity violations — this is a pure extension of an existing mechanism.
