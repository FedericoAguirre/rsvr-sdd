# Implementation Plan: Remove Status Buttons from Reservation List

**Branch**: `020-remove-status-buttons` | **Date**: 2026-06-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/020-remove-status-buttons/spec.md`

## Summary

Remove the inline "Used" and "Unused" status action buttons from all reservation list views (main list, filtered-by-slot, and HTMX partial swaps). Status badges and the reservation detail page's status change functionality are preserved. This is a pure UI cleanup — no database, backend logic, or contract changes required.

## Technical Context

**Language/Version**: Python 3.12, Django 5.0.x

**Primary Dependencies**: Django, gunicorn, whitenoise, weasyprint

**Storage**: PostgreSQL 16

**Testing**: pytest 9.1+, pytest-django 4.12+

**Target Platform**: Linux server (Docker/POSIX-compatible)

**Project Type**: Web application (server-rendered Django + HTMX + Bootstrap 5)

**Performance Goals**: N/A — removing buttons reduces DOM size, no regression possible.

**Constraints**: Status badges must remain visible. Detail page's status forms must remain functional.

**Scale/Scope**: Single gym operation, <1000 reservations/day. Change is purely visual — three template files edited.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1 — Code Quality (PASS)
- **Principle**: No dead code, no unresolved TODOs, YAGNI applied rigorously.
- **Impact**: Dead code is being removed (the inline buttons in three template files). No new code introduced. YAGNI fully respected — removing unused functionality.
- **Justification**: Trivial — templates are edited, no formatting or lint issues possible for deletions.

### Gate 2 — Testing Standards — NON-NEGOTIABLE (PASS)
- **Principle**: TDD mandatory. Tests must be written first.
- **Impact**: Feature involves only deletions. Existing tests that verified button presence must be updated. Tests for the detail page's status change must continue to pass unchanged.
- **Justification**: Existing 102 tests must be verified. Tests that assert button existence need removal. No new tests required (deletion-only feature).

### Gate 3 — User Experience Consistency (PASS)
- **Principle**: All user-facing text translated. Consistent formatting.
- **Impact**: Buttons being removed already had proper `{% translate %}` wrapping. Status badges remain. No new user-facing strings.
- **Justification**: No i18n impact — only removing elements, not adding.

### Gate 4 — Performance Requirements (PASS)
- **Principle**: Measurable performance criteria before implementation.
- **Impact**: Removing buttons reduces page size and DOM complexity. Performance unambiguously improves or stays neutral.
- **Justification**: No performance regression possible.

### Gate 5 — Development Workflow (PASS)
- **Principle**: Specify → Plan → Tasks → Implement. Feature branch sequential numbering. Atomic commits.
- **Impact**: Single atomic change (removing buttons from three templates). Independently testable by visual inspection and existing test suite.
- **Justification**: Branch follows `###-feature-name` convention. Independent user story.

## Project Structure

### Documentation (this feature)

```text
specs/020-remove-status-buttons/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (N/A — no data changes)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A — no contract changes)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── reservations/
│       ├── templates/
│       │   └── reservations/
│       │       ├── reservation_list.html           # Remove inline Used/Unused buttons
│       │       ├── reservation_list_by_slot.html    # Remove inline Used/Unused buttons
│       │       └── partials/
│       │           └── reservation_row.html         # Remove inline Used/Unused buttons
│       └── views.py                                 # No change (detail page still uses the view)
└── tests/
    └── test_reservations_list.py                    # Update tests that check for button presence
```

**Structure Decision**: All changes are within the existing `reservations` app template directory. No new files — only deletions from three existing templates. The `reservation_change_status` view is preserved for detail-page usage. Tests live in the existing test file.

## Complexity Tracking

No complexity violations — this feature removes code, does not add any. YAGNI, KISS, and all constitution principles are respected without exception.
