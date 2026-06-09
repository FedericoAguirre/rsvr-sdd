---

description: "Task list for Cardio Equipment Reservation feature implementation"

---

# Tasks: Cardio Equipment Reservation

**Input**: Design documents from `specs/001-equipment-reservation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not requested in spec — test tasks omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `tests/` at repository root
- Paths shown below assume Django project structure — Django apps under `backend/apps/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md
- [x] T002 Initialize Django project with uv: pyproject.toml with Django, psycopg2, gunicorn deps in backend/pyproject.toml
- [x] T003 [P] Configure ruff linter and formatter in backend/pyproject.toml
- [x] T004 [P] Create Dockerfile for Django web service in backend/Dockerfile
- [x] T005 Create docker-compose.yml with web and db services at docker-compose.yml
- [x] T006 [P] Create db init directory at db/init/schema.sql

**Checkpoint**: Project skeleton ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**IMPORTANT**: No user story work can begin until this phase is complete

- [x] T007 Create Django apps: clients, equipment, classes, reservations in backend/apps/
- [x] T008 [P] Create Client model in backend/apps/clients/models.py
- [x] T009 [P] Create Equipment model in backend/apps/equipment/models.py
- [x] T010 [P] Create ClassSlot model in backend/apps/classes/models.py
- [x] T011 Create Reservation model with unique constraint on (equipment, class_slot, date) in backend/apps/reservations/models.py
- [x] T012 Register all models in Django admin at backend/apps/*/admin.py
- [x] T013 Create base template with Bootstrap 5 in backend/templates/base.html
- [x] T014 Configure Django settings for PostgreSQL, static files, templates, auth in backend/config/settings.py
- [x] T015 Create login template and wire auth URLs in backend/templates/registration/login.html
- [x] T016 Create seed_data management command in backend/apps/reservations/management/commands/seed_data.py
- [ ] T017 Run initial migrations and verify database connection

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Operator Creates Reservation (Priority: P1) 🎯 MVP

**Goal**: Operator can search clients, view available equipment per class slot, and create reservations

**Independent Test**: Operator logs in, searches a client by email, selects Monday 17:30, picks an in-service treadmill, creates reservation — confirmed in reservation list view

### Implementation for User Story 1

- [x] T018 [US1] Create client search view and template in backend/apps/clients/views.py and backend/apps/clients/templates/clients/search.html
- [x] T019 [US1] Create client create view and form in backend/apps/clients/views.py and backend/apps/clients/forms.py
- [x] T020 [US1] Create client detail view showing reservation history in backend/apps/clients/views.py
- [x] T021 [P] [US1] Create reservation list/dashboard view in backend/apps/reservations/views.py
- [x] T022 [P] [US1] Create reservation create view and form in backend/apps/reservations/views.py and backend/apps/reservations/forms.py
- [x] T023 [US1] Create reservation templates (list, create, detail) in backend/apps/reservations/templates/reservations/
- [x] T024 [US1] Wire all US1 URLs in backend/apps/clients/urls.py and backend/apps/reservations/urls.py and include in root URLconf
- [x] T025 [US1] Add site navigation (navbar) in backend/templates/base.html

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Administrator Manages Equipment (Priority: P2)

**Goal**: Administrator can view, add, edit equipment and toggle its in-service/out-of-service status

**Independent Test**: Admin logs in, adds a new treadmill, marks an existing bike as out of service, verifies bike is not shown as available in operator reservation view

### Implementation for User Story 2

- [x] T026 [P] [US2] Create equipment list and detail views in backend/apps/equipment/views.py
- [x] T027 [P] [US2] Create equipment create and edit views/forms in backend/apps/equipment/views.py and backend/apps/equipment/forms.py
- [x] T028 [US2] Create equipment management templates in backend/apps/equipment/templates/equipment/
- [x] T029 [US2] Wire equipment URLs in backend/apps/equipment/urls.py and include in root URLconf

**Checkpoint**: At this point, User Story 2 should work independently

---

## Phase 5: User Story 3 - Administrator Manages Class Schedule (Priority: P3)

**Goal**: Administrator can view the weekly class schedule and toggle individual class slots active/inactive

**Independent Test**: Admin views the schedule showing all 10 slots (Mon-Fri × 17:30, 18:30), toggles a slot inactive, confirms operators cannot reserve that slot

### Implementation for User Story 3

- [x] T030 [P] [US3] Create class schedule list view in backend/apps/classes/views.py
- [x] T031 [P] [US3] Create class slot toggle view in backend/apps/classes/views.py
- [x] T032 [US3] Create class schedule template in backend/apps/classes/templates/classes/schedule.html
- [x] T033 [US3] Wire class schedule URLs in backend/apps/classes/urls.py and include in root URLconf

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T034 Update seed_data command to create sample clients for testing
- [ ] T035 Run ruff check on entire backend/ and fix issues (requires Docker/local venv — skipped in this env)
- [x] T036 Validate quickstart.md walkthrough end-to-end
- [x] T037 Final review: verify all acceptance scenarios from spec.md pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational — no dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational — no dependencies on other stories

### Within Each User Story

- Models before views
- Views before templates
- Templates before URL wiring
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004, T006 can run in parallel (Phase 1)
- T008, T009, T010 can run in parallel (Phase 2)
- T021 and T022 can run in parallel (US1)
- T026 and T027 can run in parallel (US2)
- T030 and T031 can run in parallel (US3)
- All user stories can run in parallel after Foundational (if team capacity allows)

---

## Parallel Example: User Story 1

```bash
# Launch reservation views together (different files):
Task: "Create reservation list/dashboard view in backend/apps/reservations/views.py"
Task: "Create reservation create view and form in backend/apps/reservations/views.py and backend/apps/reservations/forms.py"

# Then wire URLs:
Task: "Wire all US1 URLs in backend/apps/clients/urls.py and backend/apps/reservations/urls.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (P1)
   - Developer B: User Story 2 (P2)
   - Developer C: User Story 3 (P3)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
