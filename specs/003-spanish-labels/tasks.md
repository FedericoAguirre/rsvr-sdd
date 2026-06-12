# Tasks: Spanish Labels Translation

**Input**: Design documents from `specs/003-spanish-labels/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Test tasks are included per TDD mandate (Constitution II. Testing Standards). Each user story phase starts with tests that MUST fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Django project**: `backend/apps/`, `backend/templates/`, `backend/config/`, `tests/`
- All paths relative to repo root unless noted

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Enable Django i18n framework and prepare locale directory

- [x] T001 [P] Configure Django i18n settings in backend/config/settings.py (LANGUAGE_CODE='es', LANGUAGES, LOCALE_PATHS, LocaleMiddleware, USE_L10N=True)
- [x] T002 [P] Create locale directory structure at backend/locale/es/LC_MESSAGES/ with .gitkeep
- [x] T003 Update HTML lang attribute from "en" to "es" in backend/templates/base.html

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add i18n module imports and template tags needed by all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Add `{% load i18n %}` to all 12 HTML templates (base.html, login.html, equipment_list.html, equipment_detail.html, equipment_form.html, reservation_list.html, reservation_detail.html, reservation_form.html, search.html, client_detail.html, client_form.html, schedule.html)
- [x] T005 Import `gettext` and `gettext_lazy` in all Python source files that contain user-facing strings (apps/equipment/models.py, apps/equipment/views.py, apps/reservations/models.py, apps/reservations/views.py, apps/clients/models.py, apps/clients/views.py, apps/clients/forms.py, apps/classes/models.py, apps/classes/views.py, apps/reservations/management/commands/seed_data.py)

**Checkpoint**: Foundation ready — i18n wrappers can now be added to individual files

---

## Phase 3: User Story 1 — Navigate the application in Spanish (Priority: P1) 🎯 MVP

**Goal**: All navigation elements, page titles, and headings display in Spanish

**Independent Test**: Load each page and verify the navbar brand displays "Reserva de Cardio" and nav links display as "reservaciones", "Clientes", "Equipos", "Horario", "Admin", "Cerrar sesión"

### Tests for User Story 1 (TDD — MUST fail before implementation) ⚠️

- [x] T006 [US1] Write test that loads each page and verifies navbar brand "Reserva de Cardio" and nav link text in Spanish in tests/test_i18n.py

### Implementation for User Story 1

- [x] T007 [P] [US1] Wrap strings in backend/templates/base.html with {% translate %} tags (navbar brand, nav links, logout button, page title)
- [x] T008 [P] [US1] Wrap strings in backend/templates/registration/login.html with {% translate %} tags (Login heading, submit button)

**Checkpoint**: Navigation and login pages display in Spanish — basic application orientation is functional

---

## Phase 4: User Story 2 — Manage equipment inventory in Spanish (Priority: P1)

**Goal**: Equipment management pages display all labels, buttons, statuses in Spanish

**Independent Test**: Create, view, edit, and list equipment items and verify all table headers, form labels, buttons, and status indicators display Spanish text

### Tests for User Story 2 (TDD — MUST fail before implementation) ⚠️

- [x] T009 [US2] Write test that verifies Spanish text on equipment list, detail, and form pages in tests/test_i18n.py

### Implementation for User Story 2

- [x] T010 [P] [US2] Wrap strings in backend/apps/equipment/templates/equipment/equipment_list.html with {% translate %} tags (headers: Name/Type/Status, buttons: View/Edit/Add Equipment)
- [x] T011 [P] [US2] Wrap strings in backend/apps/equipment/templates/equipment/equipment_detail.html with {% translate %} tags (labels: Type/Status/Notes, buttons: Edit/Back)
- [x] T012 [P] [US2] Wrap strings in backend/apps/equipment/templates/equipment/equipment_form.html with {% translate %} tags (heading, Save/Cancel buttons)
- [x] T013 [P] [US2] Translate model choices with gettext_lazy in backend/apps/equipment/models.py (EQUIPMENT_TYPES: Treadmill/Stationary Bike/Elliptical/Rowing Machine/Other; STATUS_CHOICES: In Service/Out of Service; verbose_name_plural)
- [x] T014 [US2] Translate view success messages with gettext in backend/apps/equipment/views.py ("Equipment added.", "Equipment updated.")

**Checkpoint**: Equipment management fully functional in Spanish

---

## Phase 5: User Story 3 — Manage reservations in Spanish (Priority: P1)

**Goal**: Reservation creation, listing, and detail views display all labels in Spanish

**Independent Test**: Create, list, and view reservations and verify all table headers, form fields, labels, messages, and empty states display in Spanish

### Tests for User Story 3 (TDD — MUST fail before implementation) ⚠️

- [x] T015 [US3] Write test that verifies Spanish text on reservation list, form, and detail pages in tests/test_i18n.py

### Implementation for User Story 3

- [x] T016 [P] [US3] Wrap strings in backend/apps/reservations/templates/reservations/reservation_list.html with {% translate %} tags (headers: Date/Client/Class/Equipment, button: New Reservation/Filter, empty state)
- [x] T017 [P] [US3] Wrap strings in backend/apps/reservations/templates/reservations/reservation_detail.html with {% translate %} tags (labels: Client/Equipment/Class/Date/Created by/Notes, Back button)
- [x] T018 [P] [US3] Wrap strings in backend/apps/reservations/templates/reservations/reservation_form.html with {% translate %} tags (heading, Create Reservation/Cancel buttons)
- [x] T019 [P] [US3] Translate model __str__ with gettext in backend/apps/reservations/models.py
- [x] T020 [US3] Translate view success message with gettext in backend/apps/reservations/views.py ("Reservation created.")

**Checkpoint**: Reservation management fully functional in Spanish

---

## Phase 6: User Story 4 — Search and manage clients in Spanish (Priority: P2)

**Goal**: Client search, detail, and creation pages display all labels in Spanish

**Independent Test**: Search, view, and create clients and verify all headers, form labels, table headers, buttons, and empty states display in Spanish

### Tests for User Story 4 (TDD — MUST fail before implementation) ⚠️

- [x] T021 [US4] Write test that verifies Spanish text on client search, detail, and form pages in tests/test_i18n.py

### Implementation for User Story 4

- [x] T022 [P] [US4] Wrap strings in backend/apps/clients/templates/clients/search.html with {% translate %} tags (heading, Search button, New Client button, results heading, table headers: Name/Email/Mobile, empty state)
- [x] T023 [P] [US4] Wrap strings in backend/apps/clients/templates/clients/client_detail.html with {% translate %} tags (labels: Email/Mobile, buttons: New Reservation/Back to Search, heading: Reservation History, empty state)
- [x] T024 [P] [US4] Wrap strings in backend/apps/clients/templates/clients/client_form.html with {% translate %} tags (heading, Save/Cancel buttons)
- [x] T025 [P] [US4] Translate form labels and placeholders with gettext_lazy in backend/apps/clients/forms.py (ClientSearchForm: label "Search by email or mobile", placeholder "Email or mobile number...")
- [x] T026 [US4] Translate view success message with gettext in backend/apps/clients/views.py ("Client {client} created.")

**Checkpoint**: Client management fully functional in Spanish

---

## Phase 7: User Story 5 — View class schedule in Spanish (Priority: P2)

**Goal**: Class schedule displays days, statuses, and action buttons in Spanish

**Independent Test**: Load the class schedule page and verify table headers, day names, status badges, and toggle buttons display in Spanish

### Tests for User Story 5 (TDD — MUST fail before implementation) ⚠️

- [x] T027 [US5] Write test that verifies Spanish text on class schedule page in tests/test_i18n.py

### Implementation for User Story 5

- [x] T028 [P] [US5] Wrap strings in backend/apps/classes/templates/classes/schedule.html with {% translate %} tags (headers: Day/Time/Status, badges: Active/Inactive, buttons: Deactivate/Activate)
- [x] T029 [P] [US5] Translate day choices and __str__ with gettext_lazy in backend/apps/classes/models.py (DAY_CHOICES: Monday-Friday, TIME_CHOICES labels, __str__ format, __str__ "inactive" suffix)
- [x] T030 [US5] Translate view success messages with gettext in backend/apps/classes/views.py ("Class slot {slot} activated.", "Class slot {slot} deactivated.")

**Checkpoint**: Class schedule fully functional in Spanish

---

## Phase 8: Translation Generation & Polish

**Purpose**: Generate translation files, add Spanish translations, compile, and verify

- [ ] T031 Run `python manage.py makemessages --all` from backend/ to extract all translatable strings into backend/locale/es/LC_MESSAGES/django.po
- [ ] T032 Fill all msgstr entries in backend/locale/es/LC_MESSAGES/django.po with Spanish translations (refer to spec acceptance scenarios for exact expected strings)
- [ ] T033 Run `python manage.py compilemessages` from backend/ to generate backend/locale/es/LC_MESSAGES/django.mo
- [ ] T034 [P] Translate CLI messages in backend/apps/reservations/management/commands/seed_data.py with gettext ("Data seeded successfully.", "Class slots already exist, skipping.", "Created {n} class slots.", "Equipment already exists, skipping.", "Created {n} equipment items.", "Clients already exist, skipping.", "Created {n} clients.", command help string)
- [ ] T035 Run full test suite (`python -m pytest`) and verify all tests pass — fix any failures
- [ ] T036 Verify no untranslated strings remain by running `makemessages --all` and checking for empty/fuzzy msgstr entries
- [ ] T037 Commit all translation artifacts (.po, .mo, Python changes, template changes)

**Checkpoint**: Feature complete — all user-facing text displays in Spanish

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories within the same priority tier (US1 US2 US3 are all P1) can proceed in parallel
  - US4 and US5 (P2) are lower priority than US1-US3
- **Translation Generation (Phase 8)**: Depends on ALL user stories being complete

### User Story Dependencies

- **US1 (P1)**: No dependencies on other stories — base.html and login.html are the base layout
- **US2 (P1)**: No dependencies on other stories — equipment app is self-contained
- **US3 (P1)**: No dependencies on other stories — reservation app is self-contained
- **US4 (P2)**: No dependencies on other stories — client app is self-contained
- **US5 (P2)**: No dependencies on other stories — classes app is self-contained

### Within Each User Story

- Tests (included per TDD) MUST be written and FAIL before implementation
- Template wraps before Python model/view wraps (to see the effect during testing)
- Story complete before moving to next priority

### Parallel Opportunities

- T001, T002 can run in parallel (different files, no dependencies)
- T004, T005 can run in parallel (different file groups)
- All user story phases (US1-US5) can run in parallel once Foundational completes
- Within a story: all [P] tasks can run in parallel (different template files or different model/view files)
- T031, T032, T033 must be sequential (makemessages → edit .po → compilemessages)
- T034 is independent of T031-T033 but must be done before T035

---

## Parallel Example: User Story 2

```bash
# Launch all template tasks for US2 together:
Task: "Wrap equipment_list.html with {% translate %} tags"
Task: "Wrap equipment_detail.html with {% translate %} tags"
Task: "Wrap equipment_form.html with {% translate %} tags"

# Launch all Python tasks for US2 together:
Task: "Translate model choices with gettext_lazy in equipment/models.py"
Task: "Translate success messages in equipment/views.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Navigation in Spanish)
4. **STOP and VALIDATE**: Verify navbar, nav links, page titles, and login page display in Spanish
5. Deploy/demo if ready — basic navigation is usable

### Incremental Delivery

1. Complete Setup + Foundational → i18n framework ready
2. Add US1 → Navigation in Spanish → Deploy/Demo (MVP!)
3. Add US2 → Equipment in Spanish → Deploy/Demo
4. Add US3 → Reservations in Spanish → Deploy/Demo
5. Add US4 → Clients in Spanish → Deploy/Demo
6. Add US5 → Schedule in Spanish → Deploy/Demo
7. Each story adds Spanish coverage without breaking previous translations

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Navigation) + US5 (Schedule)
   - Developer B: US2 (Equipment) + US4 (Clients)
   - Developer C: US3 (Reservations)
3. All stories converge at Phase 8 for final .po generation
4. One person fills .po translations and compiles — rest translate seed data / test

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable (individual page Spanish verification)
- Verify tests fail before implementing (TDD mandate)
- The .po file is generated ONCE at Phase 8 after all tags are in place — DO NOT run makemessages before Phase 8
- Commit after each task or logical group using `git add` + `git commit`
- Stop at any checkpoint to validate story independently
- Avoid: editing .po file before all tags are in place (will miss strings)
- Cross-story dependencies: none — each app is independent
