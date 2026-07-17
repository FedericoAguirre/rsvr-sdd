# Tasks: Change navigation bar menu order

**Input**: Design documents from `specs/046-change-menu-order/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

N/A — no project initialization needed. The project is already set up with Django, Bootstrap 5, and i18n.

---

## Phase 2: Foundational (Blocking Prerequisites)

N/A — no blocking infrastructure prerequisites. This is a single template reorder with no new models, databases, or services.

---

## Phase 3: User Story 1 - Reorder navigation bar items (Priority: P1) 🎯 MVP

**Goal**: Reorder the navigation bar menu items in `backend/templates/base.html` from their current order (Reservations, Clients, Equipment, Schedule, Payments, Reports, Admin, Logout) to: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión.

**Independent Test**: Load any authenticated page and verify the nav `<li>` elements appear in the specified order. The test in `backend/tests/test_i18n.py` covers this.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (TDD per Constitution §II)**

- [ ] T001 [P] [US1] Write TDD test for nav menu item order in `backend/tests/test_i18n.py` — render any authenticated page, extract nav `<li>` items, and assert left-to-right order: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión. Confirm test FAILS before implementation.

### Implementation for User Story 1

- [ ] T002 [US1] Reorder `<li>` elements in `backend/templates/base.html` lines 17-40 to match: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión — move each `<li>` block (including `{% if %}` wrappers for conditional items) as a complete unit. Confirm T001 now PASSES.
- [ ] T003 [US1] Run full test suite (`docker compose exec web uv run manage.py test`) and lint to confirm zero regressions

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T004 Update feature todo file: move `ai/features/todos/20-change-menu-order.md` to `ai/features/done/`
- [ ] T005 Save AI session file to `ai/sessions/`
- [ ] T006 [P] Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A — no setup needed
- **Foundational (Phase 2)**: N/A — no foundational tasks
- **User Stories (Phase 3)**: Only User Story 1 — single story
- **Polish (Final Phase)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start immediately — single file change

### Within User Story 1

- Tests MUST be written first and FAIL before implementation (TDD)
- Implementation follows test
- Verification (full suite) after implementation

### Parallel Opportunities

- T001 is standalone (test file) — no parallel opportunities for a single-file change
- T002 depends on T001 passing
- T003 depends on T002
- T004, T005, T006 can run in parallel in the polish phase

---

## Parallel Example: User Story 1

```bash
# Test first (TDD — must fail):
docker compose exec web uv run manage.py test backend.tests.test_i18n.NavMenuOrderTest --verbosity=2
# Expected: FAIL (no order test yet)

# After implementation:
docker compose exec web uv run manage.py test backend.tests.test_i18n --verbosity=2
# Expected: PASS

# Full suite:
docker compose exec web uv run manage.py test --verbosity=2
# Expected: zero regressions
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. T001 — Write TDD test (expect failure)
2. T002 — Reorder template (test should pass)
3. T003 — Full suite verification
4. T004-T006 — Polish and close out

### Environment Reference

- **Run tests**: `docker compose exec web uv run manage.py test`
- **Run specific test**: `docker compose exec web uv run manage.py test backend.tests.test_i18n --verbosity=2`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
