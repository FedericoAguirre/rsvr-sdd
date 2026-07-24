# Tasks: List Unassociated Reservations on Payments Page

**Input**: Design documents from `specs/051-list-unassociated-reservations/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Django backend**: `backend/apps/`, `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and context setup

No setup tasks required. This feature uses only existing Django ORM patterns — no new libraries, utilities, or dependencies.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites — existing view (`ClientPaymentHistoryView`) and template (`payment_list.html`) are ready to extend.

---

## Phase 3: User Story 1 — View Unassociated Reservations for a Client (Priority: P1) 🎯 MVP

**Goal**: Staff user visits `/payments/client/<int:client_id>/` and sees the client's reservations that have no payment association, alongside the existing payment history.

**Independent Test**: Navigate to the `payments/client/{client_id}/` page for a client who has a mix of associated and unassociated reservations. Verify only unassociated reservations appear in the unassociated section, the payment history list is unaffected, and the empty-state message shows when no unassociated reservations exist.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T001 [P] [US1] Test unassociated reservations appear on client payments page in `backend/tests/test_payments_unassociated_reservations.py`
- [X] T002 [P] [US1] Test associated reservations do NOT appear on client payments page in `backend/tests/test_payments_unassociated_reservations.py`
- [X] T003 [P] [US1] Test empty state when all reservations are associated in `backend/tests/test_payments_unassociated_reservations.py`
- [X] T004 [P] [US1] Test empty state when client has no reservations in `backend/tests/test_payments_unassociated_reservations.py`
- [X] T005 [P] [US1] Test existing payment history list is unaffected on client payments page in `backend/tests/test_payments_unassociated_reservations.py`

### Implementation for User Story 1

- [X] T006 [US1] Extend `ClientPaymentHistoryView.get_context_data()` in `backend/apps/payments/views.py` to query and include unassociated reservations (`Reservation.objects.filter(client_id=..., payment_links=None).select_related("equipment", "class_slot").order_by("-date", "class_slot__time")`)
- [X] T007 [US1] Add "Reservations without payment" section to `backend/apps/payments/templates/payments/payment_list.html` with table/card showing date, class slot, equipment, and status for each unassociated reservation
- [X] T008 [US1] Add empty-state message in `backend/apps/payments/templates/payments/payment_list.html` when no unassociated reservations exist for the client

**Checkpoint**: US1 should be fully functional — staff can see unassociated reservations on the client payments page, with proper empty-state handling

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: i18n, cleanup, and final verification

- [X] T009 [P] Extract new user-visible strings with `django-admin makemessages -l es`
- [X] T010 [P] Translate new strings in `backend/locale/es/LC_MESSAGES/django.po`
- [X] T011 Run `django-admin compilemessages` to compile translations
- [X] T012 Run full test suite: `docker compose exec web uv run pytest`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — not applicable (no setup tasks)
- **Foundational (Phase 2)**: No dependencies — not applicable (no blocking prerequisites)
- **User Story 1 (Phase 3)**: Can start immediately
- **Polish (Phase 4)**: Depends on US1 being complete

### User Story Dependencies

- **US1 (P1)**: Single story — no dependencies on other stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Test → Implement → Verify cycle per story

### Parallel Opportunities

- All tests for US1 (T001–T005) marked [P] can run in parallel
- T009 and T010 in Phase 4 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test unassociated reservations appear on page in backend/tests/test_payments_unassociated_reservations.py"
Task: "Test associated reservations do NOT appear in backend/tests/test_payments_unassociated_reservations.py"
Task: "Test empty state (all associated) in backend/tests/test_payments_unassociated_reservations.py"
Task: "Test empty state (no reservations) in backend/tests/test_payments_unassociated_reservations.py"
Task: "Test existing payment history unaffected in backend/tests/test_payments_unassociated_reservations.py"

# Implementation is sequential (view → template):
Task: "Extend ClientPaymentHistoryView in backend/apps/payments/views.py"
Task: "Add unassociated reservations section to backend/apps/payments/templates/payments/payment_list.html"
Task: "Add empty-state message to backend/apps/payments/templates/payments/payment_list.html"
```

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. Complete Phase 3: User Story 1 (tests + implementation)
2. **STOP and VALIDATE**: Test US1 independently
3. Complete Phase 4: Polish (i18n + final test suite)

### Environment Reference

- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Run tests**: `docker compose exec web uv run pytest`
- **Run specific tests**: `docker compose exec web uv run pytest backend/tests/test_payments_unassociated_reservations.py -v`
- **i18n extract**: `docker compose exec web uv run manage.py makemessages -l es`
- **i18n compile**: `docker compose exec web uv run manage.py compilemessages`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All user-visible strings MUST use i18n (Principle III — NON-NEGOTIABLE)
