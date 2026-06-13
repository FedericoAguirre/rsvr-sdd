# Implementation Plan: Add Client Search by Name

**Branch**: `005-add-client-search` | **Date**: 2026-06-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-add-client-search/spec.md`

## Summary

Add name-based search to the existing `clients/search/` page so Operators can find clients by first or last name (partial, case-insensitive, min 3 chars) alongside the existing email/mobile search. Results update in real-time via HTMX with a ~300ms debounce, matched text is highlighted with bold + background color, and a "Client NOT FOUND" message appears when no results match. The feature reuses the existing Django view, adds HTMX for dynamic updates, and requires no schema changes.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: HTMX (via CDN script), Django ORM for queries, Bootstrap 5 for existing styling

**Storage**: PostgreSQL 16 — no schema changes; Client model already exists with first_name and last_name fields

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker container)

**Project Type**: Web application (Django + Bootstrap/HTML5 + HTMX)

**Performance Goals**: Search results render within 2s for up to 1,000 clients; no measurable regression on existing email/mobile search flow

**Constraints**: Must not break existing search-by-email/mobile functionality; all user-facing strings already use Django i18n (`{% translate %}` / `_()`); minimum 3 characters before name search triggers; search is case-insensitive; must follow WCAG 2.1 AA

**Scale/Scope**: ~20–30 lines of new/modified Python, one template update, one partial template, one new test file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Evaluation

| Principle | Assessment | Status |
|-----------|-----------|--------|
| I. Code Quality | Feature is small and focused; adds one new dependency (HTMX via CDN); follows existing view patterns (function-based views, `@login_required`) | ✅ PASS |
| II. Testing Standards (NON-NEGOTIABLE) | Tests for name search, case insensitivity, 3-char minimum, highlighting, "Client NOT FOUND" message, and existing search regression must be written before implementation | ✅ PASS |
| III. User Experience Consistency | Search uses the existing Bootstrap form and table styles; HTMX provides real-time updates matching modern UX expectations; highlighting follows the existing translated label patterns; "Client NOT FOUND" message matches the existing "No clients found" empty state pattern | ✅ PASS |
| IV. Performance Requirements | Debounced queries prevent excessive DB hits; Django ORM filters operate efficiently on indexed columns; target <2s response for 1,000 clients | ✅ PASS |

**Result**: All gates pass. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/005-add-client-search/
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
│   └── clients/
│       ├── views.py                      # Add name filter to client_search; add htmx_search endpoint
│       └── templates/
│           └── clients/
│               ├── search.html           # Add HTMX attributes to form, result partial include
│               └── _search_results.html  # NEW — partial for HTMX swap
├── templates/
│   └── base.html                         # Add HTMX script tag
└── tests/
    └── test_client_search_name.py        # NEW — name search, highlighting, NOT FOUND tests
```

**Structure Decision**: Standard Django app layout. HTMX is loaded via CDN in base.html. The feature touches the `clients` app — one view update, two template changes (one new partial), and one new test file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations — standard Django ORM query extension plus HTMX partial rendering.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
