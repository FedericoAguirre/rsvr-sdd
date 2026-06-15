---

description: "Task list for translating English tags into Spanish"
---

# Tasks: Translate English Tags into Spanish

**Input**: Design documents from `specs/011-translate-english-tags/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not requested in this feature — tests omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Django project**: `backend/apps/`, `backend/locale/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No project setup needed — Django project, i18n, and templates all exist. Skip to user stories.

No tasks required.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational blockers. Both user stories operate on independent files and can proceed immediately.

No tasks required.

---

## Phase 3: User Story 1 - Client search localized UI (Priority: P1) 🎯 MVP

**Goal**: All 7 English UI strings in the `clients/search` endpoint display in Spanish.

**Independent Test**: Navigate to `clients/search/` and verify these strings appear in Spanish:
- "Empiece a escribir para buscar clientes..." (placeholder)
- "Búsqueda..." (loading indicator)
- "Buscar clientes..." (search input placeholder)
- "Filtrado por" (active filter label)
- "Cliente NO ENCONTRADO" (not found message)
- "Siguiente" (next button)
- "Último" (last button)

### Implementation for User Story 1

- [x] T001 [P] [US1] Add "Searching..." → "Búsqueda..." entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T002 [P] [US1] Add "Search clients..." → "Buscar clientes..." entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T003 [P] [US1] Add "Filtered by \"%(q)s\"" → "Filtrado por \"%(q)s\"" entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T004 [P] [US1] Add "Client NOT FOUND" → "Cliente NO ENCONTRADO" entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T005 [P] [US1] Add "Start typing to search clients..." → "Empiece a escribir para buscar clientes..." entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T006 [P] [US1] Add "Next" → "Siguiente" entry in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T007 [P] [US1] Add "Last" → "Último" entry in `backend/locale/es/LC_MESSAGES/django.po`

**Checkpoint**: All 7 PO entries added. Deploy and verify clients/search page shows only Spanish text.

---

## Phase 4: User Story 2 - Equipment admin consistent Spanish (Priority: P2)

**Goal**: Equipment admin page uses Spanish "Equipo" consistently, replacing untranslated "Equipment".

**Independent Test**: Navigate to `admin/equipment/equipment/` and verify:
- "Seleccione equipo a modificar" instead of "Seleccione equipment a modificar"
- "AÑADIR EQUIPO" instead of "AÑADIR EQUIPMENT"

### Implementation for User Story 2

- [x] T008 [P] [US2] Add `verbose_name = _("Equipment")` to `Equipment.Meta` in `backend/apps/equipment/models.py`
- [x] T009 [P] [US2] Update existing "Equipment" PO entry: change `msgstr "Equipos"` to `msgstr "Equipo"` in `backend/locale/es/LC_MESSAGES/django.po`

**Checkpoint**: Equipment admin page uses "Equipo" consistently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Compile translations and verify everything works.

- [x] T010 Compile `.po` → `.mo` by running `cd backend && uv run django-admin compilemessages`
- [x] T011 Verify no compilation errors from `compilemessages`
- [x] T012 Run existing test suite to confirm no regressions: `cd backend && uv run pytest`

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 3)**: No dependencies — can start immediately
- **User Story 2 (Phase 4)**: No dependencies — can start immediately
- **Polish (Phase 5)**: Depends on both US1 and US2 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories
- **User Story 2 (P2)**: No dependencies on other stories

### Within Each User Story

- All tasks in US1 marked [P] can run in parallel (different PO entries)
- Both tasks in US2 marked [P] can run in parallel

### Parallel Opportunities

- US1 and US2 can be worked on simultaneously (different files: PO entries vs model.py + PO entry)
- All 7 US1 PO entries can be added in parallel (one task per unique msgid)
- Both US2 tasks can run in parallel (model.py edit and PO edit are independent)

---

## Parallel Example: User Story 1

```bash
# All 7 PO entries can be added in parallel (different msgids):
Task: "Add Searching... entry in django.po"
Task: "Add Search clients... entry in django.po"
Task: "Add Filtered by entry in django.po"
Task: "Add Client NOT FOUND entry in django.po"
Task: "Add Start typing entry in django.po"
Task: "Add Next entry in django.po"
Task: "Add Last entry in django.po"
```

## Parallel Example: User Story 2

```bash
# Both tasks can run in parallel:
Task: "Add verbose_name to Equipment model in models.py"
Task: "Update Equipment PO entry in django.po"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: User Story 1 (all 7 PO entries)
2. **STOP and VALIDATE**: Navigate to clients/search — all UI text must be in Spanish
3. Deploy/demo if ready

### Full Delivery

1. Complete User Story 1 → Test independently → Deploy/Demo (MVP!)
2. Complete User Story 2 → Test independently → Deploy
3. Phase 5: Compile and verify

### Parallel Team Strategy

With team capacity:
1. Developer A: User Story 1 (7 PO entries in parallel)
2. Developer B: User Story 2 (model + PO edit in parallel)
3. Either: Polish phase after both complete

---

## Notes

- All 8 PO entries must be added before `compilemessages` is run, otherwise the compile step needs to be re-run
- The existing `msgid "Equipment"` → `msgstr "Equipos"` must be changed to `msgstr "Equipo"` — this affects both the template `{% translate "Equipment" %}` (now shows "Equipo") and the new `verbose_name = _("Equipment")`
- No structural template changes needed — all templates already use `{% load i18n %}` and `{% translate %}`
- Commit after each phase or logical group
- Stop at any checkpoint to validate independently
