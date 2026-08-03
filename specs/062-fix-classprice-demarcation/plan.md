# Implementation Plan: Fix ClassPrice Demarcation on New Price Entry

**Branch**: `062-fix-classprice-demarcation` | **Date**: 2026-08-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/062-fix-classprice-demarcation/spec.md`

## Summary

Bug fix: `ClassPrice.enter_price()` creates a new price with `current=True` but never archives existing current prices. The fix adds a single `update()` call inside the existing `transaction.atomic()` block to set `current=False`, `changed_at=timezone.now()`, and `changed_by=changed_by` on all existing `current=True` records before creating the new one.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: Django 5.0.x ORM, `django.utils.timezone`

**Storage**: PostgreSQL (via Django ORM, no migration changes)

**Testing**: pytest 9.1.x with pytest-django (320 existing tests)

**Target Platform**: Web browser (desktop + mobile responsive)

**Project Type**: Web application (Django backend, server-rendered templates)

**Performance Goals**: N/A (one extra UPDATE query per price entry — negligible)

**Constraints**: Must execute within the existing `transaction.atomic()` block; no schema or migration changes

**Scale/Scope**: Single method change in `backend/apps/classes/models.py`; ~5 lines added; existing tests updated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No constitution file exists at `.specify/memory/constitution.md`. Proceeding without constitution gates.

## Project Structure

### Documentation (this feature)

```text
specs/062-fix-classprice-demarcation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
└── apps/
    └── classes/
        ├── models.py          # ClassPrice.enter_price() — fix here
        └── tests/
            └── test_classes_classprice.py  # Add/update tests
```

**Structure Decision**: Single method change in `ClassPrice.enter_price()` within `backend/apps/classes/models.py`. No new files. Existing test file `test_classes_classprice.py` gets new test cases.

## Complexity Tracking

No violations. No complexity added.
