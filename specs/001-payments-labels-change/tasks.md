---

description: "Task list for Payments Labels Change feature"

---

# Tasks: Payments Labels Change

**Input**: Design documents from `/specs/001-payments-labels-change/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested in the feature specification — test update tasks are included in the Polish phase for completeness.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root
- All file paths below are relative to repository root (`/Users/federicoaguirre/Documents/proyectos/rsvr-sdd/`)

---

## Phase 1: Setup

**Purpose**: Verify the existing project is ready for changes

- [x] T001 Verify current state of `backend/apps/payments/templates/payments/payment_list.html` — confirm existing labels and classes match `research.md` expectations

---

## Phase 2: Foundational

**Purpose**: No foundational work needed — this feature modifies an existing template; no new infrastructure, models, or dependencies required.

*No tasks in this phase.*

---

## Phase 3: User Story 1 - Updated Payment Search Labels (Priority: P1) 🎯 MVP

**Goal**: Replace the search field label from `"Buscar por cliente"` to `"Buscar Clientes"` and the placeholder from `"Buscar por nombre, correo electrónico o móvil del cliente..."` to `"Buscar clientes..."` by reusing existing i18n keys from `clients/search`.

**Independent Test**: Navigate to `/payments/` and verify the search label displays "Buscar Clientes" and the input placeholder displays "Buscar clientes...".

### Implementation for User Story 1

- [x] T002 [US1] Replace search field label in `backend/apps/payments/templates/payments/payment_list.html` — change `{% translate "Search by Client" %}` to `{% translate "Search Clients" %}`
- [x] T003 [US1] Replace search input placeholder in `backend/apps/payments/templates/payments/payment_list.html` — change `placeholder="{% translate 'Search by client name, email or mobile...' %}"` to `placeholder="{% translate 'Search clients...' %}"`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently — the payments page now uses the same wording as the clients search page.

---

## Phase 4: User Story 2 - Updated Filter Button (Priority: P1)

**Goal**: Change the search/filter submit button from `btn btn-outline-secondary` to `btn btn-primary` for visual consistency with other primary actions.

**Independent Test**: Navigate to `/payments/` and verify the search/filter button has primary (blue) styling with class `btn btn-primary`.

### Implementation for User Story 2

- [x] T004 [US2] Replace filter/submit button CSS class in `backend/apps/payments/templates/payments/payment_list.html` — change `btn btn-outline-secondary` to `btn btn-primary`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work — search field labels match clients/search and the filter button is styled as primary action.

---

## Phase 5: User Story 3 - Updated New Payment Button Style (Priority: P2)

**Goal**: Change the "Nuevo pago" button from `btn btn-primary` to `btn btn-success` to visually distinguish create actions from search actions.

**Independent Test**: Navigate to `/payments/` and verify the "Nuevo pago" button has success (green) styling with class `btn btn-success`.

### Implementation for User Story 3

- [x] T005 [US3] Replace "Nuevo pago" button CSS class in `backend/apps/payments/templates/payments/payment_list.html` — change `btn btn-primary` to `btn btn-success`

**Checkpoint**: All user stories should now be independently functional — search labels match clients/search, filter button is primary-styled, and "Nuevo pago" button is success-styled.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: i18n cleanup, test updates, and verification

- [x] T006 Update i18n translation files — run `docker compose exec web uv run django-admin makemessages --all` inside container to refresh PO file references, then remove unused `"Search by Client"` entry from `backend/locale/es/LC_MESSAGES/django.po`
- [x] T007 Compile i18n messages — run `docker compose exec web uv run django-admin compilemessages` to regenerate `backend/locale/es/LC_MESSAGES/django.mo`
- [x] T008 Update test assertions in `backend/tests/test_payments_search.py` to verify the new search label, placeholder text, and CSS classes
- [x] T009 Run full test suite — execute `docker compose run --rm web uv run pytest backend/tests/ -v` to confirm no regressions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: No tasks required for this feature
- **User Stories (Phases 3-5)**: All modify `payment_list.html` — MUST be done sequentially to avoid merge conflicts
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — starts from Phase 1
- **User Story 2 (P1)**: Depends on T003 (same file, sequential editing required)
- **User Story 3 (P2)**: Depends on T004 (same file, sequential editing required)

### Within Each Phase

- Although each phase has multiple tasks, they all modify `payment_list.html` sequentially. No parallel execution is possible within this feature since all changes touch the same single file.

### Parallel Opportunities

- **T006 (i18n extraction)** and **T008 (test updates)** could be done in parallel by different developers
- However, since all template changes must be committed first, the optimal order is sequential: T002 → T003 → T004 → T005 → (T006 + T008 parallel) → T007 → T009

---

## Parallel Example: User Story 1

```bash
# All US1 tasks must be sequential (same file):
Task: "Replace label in payment_list.html"
Task: "Replace placeholder in payment_list.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1 (label + placeholder changes)
3. **STOP and VALIDATE**: Navigate to `/payments/` and verify the label shows "Buscar Clientes" and placeholder shows "Buscar clientes..."
4. Deploy/demo if ready

### Incremental Delivery

1. Add User Story 1 → Search labels → Test independently → Demo
2. Add User Story 2 → Filter button style → Test independently → Demo
3. Add User Story 3 → "Nuevo pago" style → Test independently → Demo
4. Polish → i18n cleanup + test updates

### Environment Reference

When running tasks, always use these exact commands:
- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Run tests**: `docker compose run --rm web uv run pytest backend/tests/ -v`
- **Run specific tests**: `docker compose run --rm web uv run pytest backend/tests/test_payments_search.py -v`
- **Install packages**: `docker compose run --rm web uv add <package>`
- **Update i18n**: `docker compose exec web uv run django-admin makemessages --all`
- **Compile i18n**: `docker compose exec web uv run django-admin compilemessages`
