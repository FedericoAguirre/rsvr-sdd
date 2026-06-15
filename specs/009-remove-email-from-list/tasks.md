# Tasks: Remove Email from Client Column in Reservations List

**Input**: Design documents from `specs/009-remove-email-from-list/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, quickstart.md

**Tests**: Tests ARE included per clarification decision.

**Organization**: Tasks are grouped into one user story phase plus polish.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: User Story 1 - Admin views reservations list without email clutter (Priority: P1) 🎯 MVP

**Goal**: Remove email addresses from the client column in all three reservations list views. The column should display only the client's first and last name.

**Independent Test**: Load any reservations list page and verify the client column contains only the first and last name — no email in parentheses, no "(no contact)" fallback.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T001 [P] [US1] Test that client email is NOT present in the full reservations list HTML in `backend/tests/test_reservations_list.py`
- [X] T002 [P] [US1] Test that client email is NOT present in the by-slot reservations list HTML in `backend/tests/test_reservations_list.py`
- [X] T003 [P] [US1] Test that client email is NOT present in the PDF export in `backend/tests/test_reservations_list.py`
- [X] T004 [US1] Test that clients with missing first/last name still render cleanly without whitespace artifacts in `backend/tests/test_reservations_list.py`

### Implementation for User Story 1

- [X] T005 [P] [US1] Create `full_name` template filter in `backend/apps/reservations/templatetags/reservation_extras.py`
- [X] T006 [US1] Update `reservation_list.html` to use `{{ r.client|full_name }}` on lines 46 and 58 in `backend/apps/reservations/templates/reservations/reservation_list.html`
- [X] T007 [P] [US1] Update `reservation_list_by_slot.html` to use `{{ r.client|full_name }}` on line 26 in `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`
- [X] T008 [P] [US1] Update `reservation_list_pdf.html` to use `{{ r.client|full_name }}` on line 34 in `backend/apps/reservations/templates/reservations/reservation_list_pdf.html`

**Checkpoint**: All three reservations list views should show client names without email. Run full test suite to verify.

---

## Phase 2: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup

- [X] T009 Run full test suite: `docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings -T web python -m pytest`
- [X] T010 Manually verify the reservations list, by-slot list, and PDF export render correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 1)**: No dependencies — project infrastructure already exists
- **Polish (Phase 2)**: Depends on User Story 1 completion

### Within User Story 1

- Tests (T001–T004) MUST be written and FAIL before implementation (T005–T008)
- Template filter (T005) should be created before templates (T006–T008) use it
- Templates T006, T007, T008 can be done in parallel since they touch different files

### Parallel Opportunities

- T001/T002/T003: All test files can be written in parallel (different assertions in same file)
- T006/T007/T008: All template changes can be done in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests together:
Task: "Write tests verifying no email in any list view"

# Launch all templates together:
Task: "Update reservation_list.html"
Task: "Update reservation_list_by_slot.html"
Task: "Update reservation_list_pdf.html"
```

---

## Implementation Strategy

### MVP (Single Story)

1. Complete T001–T004: Write failing tests first (TDD)
2. Complete T005: Create `full_name` template filter
3. Complete T006–T008: Update all 3 templates
4. Complete T009: Run full test suite — all 40+ existing tests must pass
5. Complete T010: Manual verification
