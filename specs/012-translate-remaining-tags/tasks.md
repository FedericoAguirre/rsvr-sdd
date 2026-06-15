---

description: "Task list for translating remaining English tags into Spanish"
---

# Tasks: Translate Remaining Tags into Spanish

**Input**: Design documents from `specs/012-translate-remaining-tags/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Not requested — tests omitted.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Django project**: `backend/locale/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

No tasks required — project is already set up, i18n configured, template uses `{% translate %}`.

---

## Phase 2: Foundational (Blocking Prerequisites)

No foundational blockers.

---

## Phase 3: User Story 1 - Complete client search localization (Priority: P1) 🎯 MVP

**Goal**: All 4 remaining English strings in clients/search display in Spanish.

**Independent Test**: Navigate to clients/search and verify:
- "Primero" instead of "First" (pagination)
- "Anterior" instead of "Previous" (pagination)
- "Creado" instead of "Created" (table header)
- "Sí" instead of "Yes" (active status)

### Implementation for User Story 1

- [X] T001 [P] [US1] Add "Created" → "Creado" entry in `backend/locale/es/LC_MESSAGES/django.po`
- [X] T002 [P] [US1] Add "Yes,No" → "Sí,No" entry in `backend/locale/es/LC_MESSAGES/django.po`
- [X] T003 [P] [US1] Add "First" → "Primero" entry in `backend/locale/es/LC_MESSAGES/django.po`
- [X] T004 [P] [US1] Add "Previous" → "Anterior" entry in `backend/locale/es/LC_MESSAGES/django.po`

**Checkpoint**: All 4 PO entries added. Navigate to clients/search to verify.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [X] T005 Compile `.po` → `.mo` by running `cd backend && uv run django-admin compilemessages`
- [X] T006 Verify no compilation errors
- [X] T007 Run existing test suite to confirm no regressions: `cd backend && uv run pytest`

---

## Dependencies & Execution Order

- **User Story 1**: No dependencies — can start immediately
- **Polish**: Depends on US1 completion

### Parallel Opportunities

- All 4 PO entries can be added in parallel (different msgids)

---

## Parallel Example

```bash
# All 4 PO entries can be added simultaneously:
Task: "Add Created entry in django.po"
Task: "Add Yes,No entry in django.po"
Task: "Add First entry in django.po"
Task: "Add Previous entry in django.po"
```

---

## Implementation Strategy

1. Complete User Story 1 (4 PO entries — parallel)
2. Compile + verify + test
3. All done in a single pass

---

## Notes

- All 4 strings are in `_search_results.html` and already use `{% translate %}` or `_(...)` — no template changes needed
- The `Yes,No` entry uses Django's `yesno` filter which treats the comma-separated string as a single msgid
- Existing translations ("Next" → "Siguiente", "Last" → "Último") are not affected
