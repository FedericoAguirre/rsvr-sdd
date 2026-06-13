# Implementation Plan: Client List in Client Search

**Branch**: `004-client-search-list` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-client-list/spec.md`

## Summary

Add a paginated client list to the existing `clients/search/` page so Operators see all clients (with all attributes) on page load, not just search results. Each row includes an Edit link. The list paginates at 10 items when >10 clients exist. An existing client counter widget displays the total count.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Django built-in pagination (`Paginator`), Bootstrap 5 for table/button styling

**Storage**: PostgreSQL 16 — no schema changes; Client model already exists

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker container)

**Project Type**: Web application (Django + Bootstrap/HTML5)

**Performance Goals**: Page load <2s with up to 1000 clients; no measurable regression on existing search flow

**Constraints**: Must not break existing search-by-email/mobile functionality; all user-facing strings already use Django i18n (`{% translate %}` / `_()`)

**Scale/Scope**: Single template/view change; ~10–15 lines of new Python + template updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Evaluation

| Principle | Assessment | Status |
|-----------|-----------|--------|
| I. Code Quality | Feature is small and focused; no new dependencies; follows existing view patterns (function-based views, `@login_required`) | ✅ PASS |
| II. Testing Standards (NON-NEGOTIABLE) | Tests for pagination, all-attributes rendering, counter accuracy, and Edit link must be written before implementation | ✅ PASS |
| III. User Experience Consistency | List uses the existing Bootstrap table style; pagination follows Bootstrap's `Paginator` component pattern; Edit button matches existing "View" button style | ✅ PASS |
| IV. Performance Requirements | Pagination limits DB query to 10 rows per page; counter is a single `COUNT(*)` query; target <2s load for 1000 clients | ✅ PASS |

**Result**: All gates pass. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/004-client-list/
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
│       ├── views.py         # Update client_search to use Paginator, pass page_obj + all_clients
│       └── templates/
│           └── clients/
│               └── search.html  # Add all-clients table section, pagination nav, Edit button
└── tests/
    └── test_client_list.py  # NEW — pagination, counter, Edit link tests
```

**Structure Decision**: Standard Django app layout. The feature touches only the `clients` app — one view update, one template update, one new test file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations — standard Django pagination pattern throughout.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
