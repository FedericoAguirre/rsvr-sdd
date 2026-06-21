# Tasks: Add Clients Import Button

**Input**: Design documents from `specs/018-add-clients-import-button/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/template-search-page.md, quickstart.md

**Tests**: Included per constitutional TDD mandate — tests must be written FIRST and fail before implementation.

**Organization**: Tasks are grouped by user story. This feature has a single user story (P1).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` for Django project
- Paths follow the project structure from plan.md

---

## Phase 1: Setup

**Purpose**: Verify project is ready for changes

- [x] T001 Verify `clients:client-csv-upload` route exists and resolves correctly

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: i18n infrastructure that both test and implementation depend on

- [x] T002 Add `msgid "Upload Clients" / msgstr "Subir Clientes"` entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T003 Compile translations via `django-admin compilemessages`

---

## Phase 3: User Story 1 - Navigate to Client Upload from Search Page (Priority: P1) 🎯 MVP

**Goal**: Operators see a "Subir Clientes" link on the clients search page that navigates to the CSV upload page.

**Independent Test**: Visit `/clients/search/`, verify "Subir Clientes" link is present with correct href to `/clients/upload/`.

### Tests for User Story 1 (TDD — must be written first, ensure they FAIL before implementation) ⚠️

- [x] T004 [US1] Add integration test for "Subir Clientes" label on search page in `backend/tests/test_i18n.py`
- [x] T005 [US1] Verify test FAILS (target text not yet in template) by running: `python -m pytest backend/tests/test_i18n.py -v`

### Implementation for User Story 1

- [x] T006 [P] [US1] Add "Subir Clientes" navigation link to `backend/apps/clients/templates/clients/search.html` (alongside existing action buttons, using `{% url 'clients:client-csv-upload' %}` and `{% translate "Upload Clients" %}`)

### Verification for User Story 1

- [x] T007 [US1] Run all tests to confirm the "Subir Clientes" test passes: `python -m pytest backend/tests/ -v`
- [x] T008 [US1] Run linter: `ruff check backend/`

**Checkpoint**: User Story 1 complete — operators can navigate from search to upload. The feature is independently testable and deliverable.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Finalize and commit

- [x] T009 Run full test suite: `python -m pytest`
- [x] T010 Run full lint check: `ruff check backend/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Phase 2 (i18n entries in place)
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Only story — no cross-story dependencies

### Within User Story 1

- Tests MUST be written and FAIL before implementation (TDD)
- i18n entries in django.po before template changes
- Implementation before verification

### Parallel Opportunities

- T006 ([P]) is parallelizable with verification tasks but depends on T002-T003 (i18n entries compiled)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002-T003)
3. Write tests (T004-T005) — expect failure
4. Implement (T006) — tests now pass
5. Verify (T007-T008)
6. Polish (T009-T010)
7. **MVP complete — can deploy/demo**

### Incremental Delivery

Single user story — deliver in one increment after all phases complete.

---
