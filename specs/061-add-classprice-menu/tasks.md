# Tasks: Add ClassPrice Sub-Option Under "Horario" Menu

**Input**: Design documents from `specs/061-add-classprice-menu/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested. Skip test generation (only include verification via existing test suite).

**Organization**: Two user stories (P1, P2). Template-only change in a single file.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Django backend**: `backend/templates/`, `backend/apps/`
- Paths are relative to repository root

---

## Phase 1: User Story 1 - Access ClassPrice via Horario Dropdown (Priority: P1)

**Goal**: Convert the "Horario" flat link to a Bootstrap dropdown with "Horario de Clases" and "Precios" options.

**Independent Test**: Log in with `classes.view_classslot` permission, click "Horario" — dropdown appears with both links. Both navigate to correct pages.

### Implementation for User Story 1

- [x] T001 [US1] Replace flat "Schedule" link (line 28) with dropdown containing "Class Schedule" and "Class prices" links in `backend/templates/base.html`

**Checkpoint**: Dropdown appears with both links, navigation works for both options.

---

## Phase 2: User Story 2 - Menu Hides When No Permission (Priority: P2)

**Goal**: Verify the "Horario" dropdown remains hidden for users without `classes.view_classslot` permission.

**Independent Test**: Log in without `classes.view_classslot` permission — "Horario" is not visible.

### Implementation for User Story 2

- [x] T002 [US2] Verify the `{% if perms.classes.view_classslot %}` gate wraps the entire dropdown and renders correctly in `backend/templates/base.html`

**Checkpoint**: Dropdown hidden for unauthorized users, visible for authorized users.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Final verification

- [x] T003 Run existing test suite via `uv run pytest` in `backend/`
- [x] T004 Verify dropdown renders on mobile viewport (< 992px) and both links are accessible via hamburger menu

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 1)**: No dependencies — T001 is the only change needed
- **User Story 2 (Phase 2)**: Depends on T001 (verifies the same file's permission gate)
- **Polish (Phase 3)**: Depends on both Phase 1 and Phase 2

### User Story Dependencies

- **User Story 1 (P1)**: Only change — block of HTML replaced in `base.html`
- **User Story 2 (P2)**: Verification only — depends on US1 being implemented first

### Within User Stories

- All tasks are sequential (same file: `backend/templates/base.html`)

### Parallel Opportunities

None — all changes are in a single file (`base.html`). T003 and T004 can run in parallel after T001/T002 are done.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001: Replace flat link with dropdown in `base.html`
2. Complete T002: Verify permission gate
3. **STOP and VALIDATE**: Dropdown works, both links navigate correctly, permissions enforced
4. Complete T003: Run test suite
5. Complete T004: Mobile verification

### Environment Reference

- **Run server**: `cd backend && uv run python manage.py runserver`
- **Run tests**: `cd backend && uv run pytest`
- **Run checks**: `cd backend && uv run python manage.py check`

---

## Notes

- Single file change: `backend/templates/base.html` line 27-29
- Pattern to follow: "Reportes" dropdown at lines 31-36
- All i18n translations already exist in `django.po`
- All URLs already exist (`classes:class-schedule`, `classes:price-list`)
- No migration, no new views, no new models needed
- Bootstrap 5.3 CDN already loaded in base template
