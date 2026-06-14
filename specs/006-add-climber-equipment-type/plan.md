# Implementation Plan: Add Climber Equipment Type

**Branch**: `007-add-climber-equipment-type` | **Date**: 2026-06-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/006-add-climber-equipment-type/spec.md`

## Summary

Add "Climber (Escaladora)" as the first/default option in the Equipment model's EQUIPMENT_TYPES list, and seed 30 Climber equipment records (E01–E30) via data migration.

## Technical Context

**Language/Version**: Python 3.12+, Django 5.0.x

**Primary Dependencies**: django, psycopg2 (PostgreSQL adapter)

**Storage**: PostgreSQL 16 — Equipment model persists EQUIPMENT_TYPES choices as a CharField

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (production), macOS (development)

**Project Type**: Web application (Django + Bootstrap/HTMX)

**Performance Goals**: N/A — trivial change (single enum option + one-time seed)

**Constraints**: New type must be first in the list to act as default; seed migration must be reversible

**Scale/Scope**: 30 seed equipment records, 1 new enum option

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Justification |
|------|--------|---------------|
| I. Code Quality | ✅ PASS | No lint/structure concerns — single-file model change + standard migration |
| II. Testing Standards | ✅ PASS | 29 existing tests pass; no new test files needed (feature already implemented) |
| III. UX Consistency | ✅ PASS | EQUIPMENT_TYPES is rendered dynamically by Django forms/admin — no template changes needed; i18n labels already handled by model definiton |
| IV. Performance | ✅ PASS | No measurable performance impact |
| Technology Constraints | ✅ PASS | Python/Django stack unchanged |
| Development Workflow | ✅ PASS | Sequential branch naming followed (007) |

## Project Structure

### Documentation (this feature)

```text
specs/006-add-climber-equipment-type/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code

```text
backend/
├── apps/equipment/
│   ├── models.py                    # EQUIPMENT_TYPES list updated
│   └── migrations/
│       └── 0002_seed_climber_equipments.py  # New data migration
```

## Complexity Tracking

No constitution violations — no complexity justification needed.
