# Tasks: Reports Menu Option

**Input**: Design documents from `specs/024-reports-menu/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per project constitution (TDD mandatory). Write tests first, ensure they fail, then implement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Django monolith**: `backend/apps/`, `backend/templates/`, `backend/locale/`
- **Tests**: `backend/tests/`

---

## Phase 1: Setup

**Purpose**: Verify branch and working state

- [x] T001 Switch to branch `024-reports-menu` and verify clean working tree

---

## Phase 2: Foundational

**Purpose**: Baseline confirmation — no blocking prerequisites for this feature

**⚠️ CRITICAL**: Verify existing reports page renders before adding navigation

- [x] T002 [P] Verify `/payments/reports/` loads at `backend/apps/payments/views.py:142` (PaymentReportView exists and functional)
- [x] T003 [P] Read existing navbar structure in `backend/templates/base.html` to identify insertion point for Reports dropdown (after existing `{% translate "Payments" %}` link)

**Checkpoint**: Foundation ready — confirmed reports page works and insertion point identified.

---

## Phase 3: User Story 1 — Admin accesses reports via navigation menu (Priority: P1) 🎯 MVP

**Goal**: Administrator can navigate to the reports page via Reports → Payments in the navbar.

**Independent Test**: Log in as superuser, visit any page, confirm "Reports" dropdown appears in navbar with "Payments" sub-link, click it and confirm `/payments/reports/` loads.

### Tests for User Story 1 (TDD — MUST fail before implementation)

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementing

- [x] T004 [P] [US1] Write test asserting superuser sees "Reports" text in rendered navbar response via `assertContains` in `backend/tests/test_payments.py`
- [x] T005 [P] [US1] Write test asserting superuser sees "Payments" text (sub-link) in rendered navbar response via `assertContains` in `backend/tests/test_payments.py`
- [x] T006 [P] [US1] Write test asserting clicking "Payments" link navigates to `/payments/reports/` correctly in `backend/tests/test_payments.py`

### Implementation for User Story 1

- [x] T007 [US1] Add Bootstrap dropdown markup to navbar in `backend/templates/base.html`: Reports > Payments sub-item linking to `{% url 'payments:reports' %}` with `{% if user.is_superuser %}` guard
- [x] T008 [US1] Register i18n translations for "Reports" and "Payments" labels in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T009 [US1] Compile translations via `django-admin compilemessages` in `backend/`

**Checkpoint**: At this point, User Story 1 should be fully functional — admin sees Reports > Payments dropdown and can navigate to reports page.

---

## Phase 4: User Story 2 — Non-admin users do not see Reports menu (Priority: P2)

**Goal**: Non-administrator users do not see the Reports menu option in the navigation bar.

**Independent Test**: Log in as a regular user, visit any page, confirm "Reports" text is absent from the rendered navbar HTML.

### Tests for User Story 2 (TDD — MUST fail before implementation)

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementing

- [x] T010 [P] [US2] Write test asserting non-superuser does NOT see "Reports" text in rendered navbar response via `assertNotContains` in `backend/tests/test_payments.py`
- [x] T011 [P] [US2] Write test asserting non-superuser does NOT see "Payments" sub-link text in rendered navbar response via `assertNotContains` in `backend/tests/test_payments.py`
- [x] T012 [P] [US2] Write test asserting non-superuser can still access `/payments/reports/` directly (if already permitted) — verify existing view-level gate in `backend/tests/test_payments.py`

### Implementation for User Story 2

- [x] T013 [US2] Verify `{% if user.is_superuser %}` guard in `backend/templates/base.html` correctly hides Reports dropdown for non-superusers (already implemented in T007 — verify test passes)

**Checkpoint**: Both user stories independently testable — admin sees menu, non-admin does not.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T014 Run all tests in `backend/` — verify all assertions pass
- [x] T015 [P] Run linter (`ruff check .`) in `backend/`
- [x] T016 Run `python manage.py check --deploy` for deployment readiness
- [x] T017 Final i18n verification — confirm Spanish translations render for "Reports" and "Payments" in the UI
- [ ] T018 Commit all changes and prepare PR

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: No dependencies — can start immediately
- **US1 — Admin dropdown (Phase 3)**: Depends on Phase 2 verification
- **US2 — Non-admin visibility (Phase 4)**: Depends on Phase 3 implementation (guard is implemented in T007)
- **Polish (Final Phase)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 — no dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 implementation (the `{% if %}` guard) but tests can be written in parallel with US1 implementation

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Implementation before verification
- Story complete before moving to next priority

### Parallel Opportunities

- T002 and T003 can run in parallel (Phase 2)
- T004, T005, T006 can run in parallel (Phase 3 tests)
- T010, T011, T012 can run in parallel (Phase 4 tests)
- T015 runs independently (linting)

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 tests together (TDD — write first, expect failure):
python -c "
from django.test import TestCase
class TestReportsMenu(TestCase):
    def test_superuser_sees_reports_link(self):
        ...
"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test US1 independently — superuser sees Reports > Payments dropdown
5. Deploy/demo if ready

### Incremental Delivery

1. Phase 1 + 2 → Foundation ready
2. Add US1 (admin dropdown + i18n) → Test independently → Deploy/Demo (MVP!)
3. Add US2 (non-admin tests + guard verification) → Test independently → Deploy/Demo
4. Phase 5 (Polish) → Final deploy

### Parallel Team Strategy

With multiple developers:
1. Complete Phase 1 + 2 together
2. Once done:
   - Developer A: US1 implementation (T007, T008, T009)
   - Developer B: US2 tests (T010, T011, T012) — can be written once US1 guard is defined
3. Final polish together

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2] labels map tasks to specific user stories
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The `backend/tests/test_payments.py` file is shared — mark tasks in different phases to avoid conflicts
