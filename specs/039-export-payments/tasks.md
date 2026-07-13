# Tasks: Export Payments

**Input**: Design documents from `/specs/039-export-payments/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The project constitution mandates TDD with Red-Green-Refactor. Write tests first, ensure they FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` at repository root
- Reference structure: `backend/apps/payments/`, `backend/tests/`, `backend/locale/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Add openpyxl to project dependencies in `backend/pyproject.toml`
- [x] T002 Install new dependency: `docker compose run --rm web uv add openpyxl`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Add i18n entries for export-related strings in `backend/locale/es/LC_MESSAGES/django.po`
- [x] T004 Compile i18n messages: `docker compose exec web uv run manage.py compilemessages`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Export Payments with Date Range (Priority: P1) 🎯 MVP

**Goal**: Administrator can select a date range on the payments reports page, click "Exportar", and download an .xlsx spreadsheet containing payments within that range.

**Independent Test**: Navigate to `/payments/reports/`, select a date range with existing payments, click Exportar, and verify `pagos_YYYYMMDD_YYYYMMDD.xlsx` downloads with correct columns (Identificador, Cliente, Monto, Tipo, Fecha, Clases).

### Tests for User Story 1 (TDD — write first, ensure FAIL before implementation) ⚠️

- [x] T005 [P] [US1] Write test for successful export returning xlsx response with correct Content-Type and Content-Disposition in `backend/tests/test_payments.py`

### Implementation for User Story 1

- [x] T006 [P] [US1] Create `PaymentExportView` in `backend/apps/payments/views.py` with openpyxl write-only mode, querying filtered payments, writing columns
- [x] T007 [US1] Add export URL pattern (`payments:export`) to `backend/apps/payments/urls.py`
- [x] T008 [US1] Add "Exportar" button adjacent to "Generar reporte" in `backend/apps/payments/templates/payments/payment_reports.html` with htmx event handler that passes date params and disables button during download

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Export with No Data (Priority: P2)

**Goal**: Administrator is shown an alert when no payments exist in the selected date range, preventing an empty file download.

**Independent Test**: Select a date range with zero payments, click Exportar, and verify an error alert is shown with no file downloaded.

### Tests for User Story 2 (TDD — write first, ensure FAIL before implementation) ⚠️

- [x] T009 [P] [US2] Write test for no-data scenario returning 404 with error message in `backend/tests/test_payments.py`
- [x] T010 [P] [US2] Write test for inverted date range (start > end) returning 400 validation error in `backend/tests/test_payments.py`
- [x] T011 [P] [US2] Write test for server error during generation returning 500 with retry message in `backend/tests/test_payments.py`

### Implementation for User Story 2

- [x] T012 [US2] Add date validation (start > end → 400 error) in `backend/apps/payments/views.py`
- [x] T013 [US2] Add no-data check in `backend/apps/payments/views.py` (empty queryset → 404 with alert message)
- [x] T014 [US2] Add try/except error handling with logging and retry message in `backend/apps/payments/views.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T015 [P] Verify all i18n strings render correctly in Spanish by testing the export flow end-to-end
- [x] T016 [P] Add structured logging for export operations (who exported, date range, record count) in `backend/apps/payments/views.py`
- [x] T017 Run full test suite: `docker compose exec web uv run pytest backend/tests/test_payments.py -v` — 53 passed
- [x] T018 Verify exported file opens correctly in spreadsheet application (manual validation — verified by user)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable from US1

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD - constitution mandate)
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Tests within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test for successful export in backend/tests/test_payments.py"

# Launch implementation:
Task: "Create PaymentExportView in backend/apps/payments/views.py"
Task: "Add URL to backend/apps/payments/urls.py"
Task: "Add Exportar button to payment_reports.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (i18n setup)
3. Complete Phase 3: User Story 1 (export with date range)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Environment Reference

- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Run tests**: `docker compose exec web uv run pytest backend/tests/ -v`
- **Install packages**: `docker compose run --rm web uv add <package>`
- **Sync dependencies**: `docker compose exec web uv sync --system`
- **Compile translations**: `docker compose exec web uv run manage.py compilemessages`

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
