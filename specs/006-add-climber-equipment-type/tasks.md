---
description: "Task list for adding Climber equipment type"
---

# Tasks: Add Climber Equipment Type

**Input**: Design documents from `specs/006-add-climber-equipment-type/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/equipment/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create feature branch `007-add-climber-equipment-type` from main
- [X] T002 [P] Review existing Equipment model in `backend/apps/equipment/models.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Check existing EQUIPMENT_TYPES choices and ordering in `backend/apps/equipment/models.py`
- [X] T004 [P] Check existing migration pattern in `backend/apps/equipment/migrations/0001_initial.py`
- [X] T005 [P] Review seed data migration pattern from `backend/apps/clients/migrations/0002_seed_test_clients.py`

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 - Select Climber as Equipment Type (Priority: P1) 🎯 MVP

**Goal**: Operator/Administrator sees "Climber (Escaladora)" as the first/default option in the equipment type dropdown

**Independent Test**: Open the equipment creation form at `/equipment/create/` — the equipment type dropdown shows "Climber" as the first and pre-selected option

### Implementation for User Story 1

- [X] T006 [US1] Add `("climber", _("Climber"))` as the first entry in EQUIPMENT_TYPES in `backend/apps/equipment/models.py`
- [X] T007 [US1] Verify the existing `EquipmentForm` in `backend/apps/equipment/forms.py` picks up the new choice (no code change needed — Django ModelForm auto-renders choices)
- [X] T008 [US1] Verify templates in `backend/apps/equipment/templates/` render the new type via `get_equipment_type_display` (no code change needed — dynamic display)
- [X] T009 [US1] Run full test suite to confirm no regressions

**Checkpoint**: At this point, User Story 1 should be fully functional — the Climber option appears first in the dropdown and is pre-selected by default

---

## Phase 4: User Story 2 - Pre-seeded Climber Equipment (Priority: P1)

**Goal**: 30 Climber equipment records (E01–E30) exist immediately after running migrations

**Independent Test**: After `migrate`, query `Equipment.objects.filter(equipment_type="climber").count()` — returns 30

### Implementation for User Story 2

- [X] T010 [P] [US2] Create data migration `backend/apps/equipment/migrations/0002_seed_climber_equipments.py` with 30 Climber records named E01–E30
- [X] T011 [US2] Apply migration and verify 30 Climber records exist
- [X] T012 [US2] Test migration reversibility: run `migrate equipment 0001` and confirm climber records are removed
- [X] T013 [US2] Run full test suite to confirm no regressions

**Checkpoint**: Both user stories complete — Climber type is available as default, and 30 seeded equipments exist

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T014 [P] Update spec documentation in `specs/006-add-climber-equipment-type/`
- [X] T015 [P] Move `ai/features/todos/Add_climber_equipment_type.md` to `ai/features/done/`
- [X] T016 Verify all 29 tests pass with `pytest tests/ -v`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3–4)**: All depend on Foundational phase completion
  - US1 and US2 are independent — can run in parallel
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories — can start immediately after Foundation
- **User Story 2 (P1)**: No dependencies on other stories — can start immediately after Foundation

### Within Each User Story

- Model change before test verification
- Migration creation before migration application
- Core implementation before verification

### Parallel Opportunities

- T002 and setup tasks can run in parallel
- T003, T004, T005 can run in parallel
- US1 and US2 can be implemented in parallel (different files)

---

## Parallel Example: User Story 1

```bash
# Launch all model changes together:
Task: "Add climber to EQUIPMENT_TYPES in models.py"
Task: "Verify form and templates pick it up"

# Verify with tests:
cd backend && .venv/bin/python -m pytest tests/ -v
```

---

## Parallel Example: User Story 2

```bash
# Migration creation is single-file, no parallel needed:
Task: "Create data migration with 30 climber records"
Task: "Apply and verify" depends on creation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Climber type available)
4. **STOP and VALIDATE**: Create equipment form shows Climber as default
5. Deploy/demo if ready (type alone suffices as MVP)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

---

## Notes

- Both user stories are P1 (same priority) — implement in any order
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
