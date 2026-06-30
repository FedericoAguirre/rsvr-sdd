# Tasks: Duplicated Reservation Alert

**Input**: Design documents from `/specs/026-duplicated-reservation-alert/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included per constitutional mandate (TDD required).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/reservations/`, `backend/tests/`, `backend/locale/`

---

## Phase 1: Setup

**Purpose**: Verify environment and confirm feature branch is ready

- [x] T001 Verify on branch `026-duplicated-reservation-alert` with working Django environment
- [x] T002 Run existing test suite to confirm baseline green: `cd backend && pytest` (PDF segfault pre-existing, unrelated)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core logic that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Read existing `ReservationForm` in `backend/apps/reservations/forms.py` and study `unique_together` constraint in `backend/apps/reservations/models.py`
- [x] T004 Implement duplicate detection logic in `clean()` method of `ReservationForm` in `backend/apps/reservations/forms.py`

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Operator sees visible duplicate alert (Priority: P1) 🎯 MVP

**Goal**: When an operator adds an already-reserved equipment in the same class slot and date, a visible alert is displayed and form submission is blocked.

**Independent Test**: Create a reservation, then attempt to create another with the same equipment + class slot + date — the form must show an alert and not submit.

### Tests for User Story 1 (TDD — write first, ensure FAIL before implementation)

- [x] T005 [US1] Write unit test for `ReservationForm.clean()` duplicate detection in `backend/tests/test_reservations_form.py`
- [x] T006 [US1] Write integration test for duplicate alert display via test client in `backend/tests/test_reservations_form.py`

### Implementation for User Story 1

- [x] T007 [US1] Update `backend/apps/reservations/forms.py` — add `clean()` method that raises `ValidationError` with date, class slot, and equipment marked as UNAVAILABLE (use `gettext_lazy` for strings)
- [x] T008 [US1] Update `backend/apps/reservations/templates/reservations/reservation_form.html` — add non-field errors alert block using Bootstrap 5 `alert-warning` and `alert-dismissible`

**Checkpoint**: At this point, User Story 1 should be fully functional. The alert appears when a duplicate is detected and the form is blocked.

---

## Phase 4: User Story 2 — Alert is properly translated to Spanish (Priority: P2)

**Goal**: Spanish-speaking operators see the alert message in Spanish, consistent with the app's i18n.

**Independent Test**: Switch to Spanish locale and trigger the duplicate alert — all text must display in Spanish.

### Tests for User Story 2 (TDD — write first)

- [x] T009 [US2] Write test verifying Spanish locale renders alert text in Spanish in `backend/tests/test_reservations_form.py`

### Implementation for User Story 2

- [x] T010 [P] [US2] Extract alert strings via `django-admin makemessages -l es` from `backend/`
- [x] T011 [US2] Add Spanish translations for "UNAVAILABLE" → "NO DISPONIBLE" and the alert message template in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T012 [US2] Compile translations: `django-admin compilemessages` from `backend/`

**Checkpoint**: At this point, User Stories 1 and 2 should both work independently. The alert appears in English and Spanish based on locale.

---

## Phase 5: User Story 3 — Alert follows accessible UX patterns (Priority: P3)

**Goal**: The alert is dismissible, responsive, screen-reader friendly, and lists all conflicts.

**Independent Test**: Trigger a multi-item duplicate alert — all conflicts are listed, alert is keyboard-dismissible, and has ARIA attributes.

### Tests for User Story 3 (TDD)

- [x] T013 [US3] Write test verifying alert has `role="alert"` and ARIA attributes in `backend/tests/test_reservations_form.py`
- [x] T014 [US3] Write test verifying multi-equipment conflict lists all items in a single alert

### Implementation for User Story 3

- [x] T015 [US3] Ensure template alert block includes `role="alert"` and `aria-live="assertive"` in `backend/apps/reservations/templates/reservations/reservation_form.html`
- [x] T016 [US3] Add responsive CSS for alert display on mobile viewports (Bootstrap 5 alert is already responsive — no additional CSS needed)
- [x] T017 [US3] Verify alert supports listing multiple equipment items in a single message in `backend/apps/reservations/forms.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation that the entire feature works end-to-end

- [x] T018 Run full test suite: `cd backend && pytest` (10/10 passed)
- [x] T019 Verify no hardcoded user-visible strings remain in touched templates and forms
- [x] T020 Move `ai/features/todos/12_Duplicated_reservation_alert.md` to `ai/features/done/`
- [x] T021 Save compressed AI session file in `ai/sessions/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational completion
  - US1 (P1) → US2 (P2) → US3 (P3) in priority order
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — No dependencies on other stories
- **US2 (P2)**: Can start after Phase 2 — Depends on US1 alert message being implemented (same strings to translate)
- **US3 (P3)**: Can start after Phase 2 — Depends on US1 template being in place (adds ARIA attrs to existing alert)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Form logic before template changes
- Story complete before moving to next priority

### Parallel Opportunities

- T010 [P] (makemessages) can run in parallel with other Phase 4 tasks
- T003 and T004 (foundational reading/implementing) cannot be parallelized (read before write)

---

## Parallel Example: User Story 1

```bash
# Launch test files for US1 together:
Task: "Write unit test in backend/tests/test_reservations_form.py"
Task: "Write integration test in backend/tests/test_reservations_form.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test that duplicate alert appears and blocks form submission
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (alert logic + template) → Test independently → Deploy/Demo (MVP!)
3. Add US2 (Spanish i18n) → Test independently → Deploy/Demo
4. Add US3 (accessibility polish) → Test independently → Deploy/Demo

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The `clean()` method must use `gettext_lazy` for all user-facing strings (constitution mandate)
