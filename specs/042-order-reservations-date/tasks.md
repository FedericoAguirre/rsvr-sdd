# Tasks: Order Reservations by Date in Payment Detail

**Input**: Design documents from `/specs/042-order-reservations-date/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Single user story — this is a minimal sorting change.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Path Conventions

This is a Django web application. All source code under `backend/`.

---

## Phase 1: Setup

**Purpose**: Ensure environment is ready

- [x] T001 Verify branch `042-order-reservations-date` is active and up to date with main
- [x] T002 [P] Start Docker environment: `make restart`

---

## Phase 2: Foundational

**Purpose**: No new infrastructure needed — project is fully set up. Skip to User Story.

---

## Phase 3: User Story 1 — Sort Reservations by Date Descending (Priority: P1) 🎯 MVP

**Goal**: Payment detail page shows associated reservations sorted by date descending (most recent first), with same-date reservations sorted by class slot time descending.

**Independent Test**: Create a payment with 3+ reservations on different dates, load the detail page, and assert the most recent reservation appears first in the rendered table.

### Tests (TDD — MUST FAIL BEFORE IMPLEMENTATION)

- [x] T003 [US1] Write test asserting reservations appear in descending date order on payment detail page. Create test data with reservations on different dates and verify HTML order in `backend/tests/test_payments.py`
- [x] T004 [US1] Write test asserting same-date reservations are sorted by class slot time descending in `backend/tests/test_payments.py`
- [x] T005 [US1] Write test asserting empty reservation list renders without error (no regression) in `backend/tests/test_payments.py`

### Implementation

- [x] T006 [US1] Add `.order_by("-reservation__date", "-reservation__class_slot__time")` to the `PaymentDetailView.get_context_data()` queryset in `backend/apps/payments/views.py:130`
- [x] T007 Run tests to confirm all pass: `docker compose exec web uv run pytest tests/test_payments.py -v`

**Checkpoint**: User Story 1 is complete — payment detail page sorts reservations correctly.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T008 Run full test suite to verify no regressions: `docker compose exec web uv run pytest -v` (220 passed, 8 pre-existing failures)
- [ ] T009 Run linting: `docker compose exec web uv run ruff check apps/payments/ tests/` (ruff not available in container)
- [ ] T010 Run type checks: `docker compose exec web uv run mypy apps/payments/` (mypy not available in container)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Skipped — no infrastructure changes needed
- **User Story 1 (Phase 3)**: Depends on Setup completion only
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Single story — no cross-story dependencies

### Within User Story 1

- Tests MUST be written and FAIL before implementation
- Implement ordering change
- Verify all tests pass

### Parallel Opportunities

- T003, T004, T005 are independent test files — can be written in parallel
- T008, T009, T010 are independent verification steps — can run in parallel

---

## Parallel Example: User Story 1

```bash
# Write all tests together:
Task: "Write date-ordering test in backend/tests/test_payments.py"
Task: "Write same-date/time-ordering test in backend/tests/test_payments.py"
Task: Write empty-list regression test in backend/tests/test_payments.py"

# Verify tests fail:
docker compose exec web uv run pytest tests/test_payments.py -v

# Implement:
Edit backend/apps/payments/views.py line 130 to add .order_by()

# Verify tests pass:
docker compose exec web uv run pytest tests/test_payments.py -v
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup — verify environment
2. Phase 3: Write failing tests → implement → verify passing
3. Phase 4: Full test suite, linting, type checks

### Environment Reference

- **Run tests**: `docker compose exec web uv run pytest tests/test_payments.py -v`
- **Run all tests**: `docker compose exec web uv run pytest -v`
- **Run linting**: `docker compose exec web uv run ruff check apps/payments/ tests/`
- **Run type checks**: `docker compose exec web uv run mypy apps/payments/`
- **Start Docker**: `make restart`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story should be independently completable
- Verify tests fail before implementing
- Commit after each logical group
