# Tasks: Fix PaymentReservation ForeignKey Warning

**Input**: Design documents from `specs/060-fix-payment-fk-warning/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested. Skip test generation (only include verification via existing test suite).

**Organization**: Single user story (P1). Tasks are linear with no parallel opportunities due to sequential dependencies.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Django backend**: `backend/apps/`, `backend/config/`
- Paths are relative to repository root

---

## Phase 1: User Story 1 - No System Warnings on Startup (Priority: P1)

**Goal**: Replace `ForeignKey(unique=True)` with `OneToOneField` on `PaymentReservation.reservation` and eliminate the `fields.W342` system check warning.

**Independent Test**: Run `python manage.py check` and verify zero `fields.W342` warnings related to `PaymentReservation.reservation`.

### Implementation for User Story 1

- [x] T001 [US1] Change `reservation` field from `models.ForeignKey(unique=True)` to `models.OneToOneField` in `backend/apps/payments/models.py` (line 136-142)
- [x] T002 [US1] Generate migration via `uv run python manage.py makemigrations payments` in `backend/`
- [x] T003 [US1] Apply migration via `uv run python manage.py migrate payments` in `backend/`
- [x] T004 [US1] Verify zero warnings via `uv run python manage.py check` in `backend/`
- [x] T005 [US1] Run existing test suite via `uv run pytest` in `backend/`

**Checkpoint**: All system checks pass with zero `fields.W342` warnings and all existing tests pass.

---

## Phase 2: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup

- [ ] T006 Rebuild Docker image and verify no warnings in container: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build web && docker exec rsvr-sdd-web-1 uv run python manage.py check`

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 1)**: No dependencies — can start immediately. Tasks T001 → T002 → T003 → T004 → T005 must execute sequentially.
- **Polish (Phase 2)**: Depends on Phase 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Only story. No inter-story dependencies.

### Within User Story 1

- T001 (model change) must complete before T002 (makemigrations)
- T002 must complete before T003 (migrate)
- T003 must complete before T004 (check) and T005 (tests)

### Parallel Opportunities

None — all tasks within US1 are sequential. T004 and T005 could theoretically run in parallel after T003, but practically they should run sequentially for clear error attribution.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001: Change field type in `models.py`
2. Complete T002: Generate migration
3. Complete T003: Apply migration
4. Complete T004: Verify zero warnings
5. Complete T005: Run test suite
6. **STOP and VALIDATE**: All checks pass, all tests pass
7. Complete T006: Verify in Docker container

### Environment Reference

When running commands, use these exact patterns:

- **Run management commands**: `cd backend && uv run python manage.py <command>`
- **Run tests**: `cd backend && uv run pytest`
- **Run checks**: `cd backend && uv run python manage.py check`
- **Docker rebuild**: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build web`

---

## Notes

- Single field change — minimal risk
- Migration is a schema no-op (both field types produce identical DDL)
- No data migration needed
- Two code references to `payment_links` in `views.py` (lines 150, 238) use queryset filters — fully compatible with `OneToOneField`
- Commit after T003 (migration generated) or after T005 (all tests pass)
