# Tasks: Remove ClassPrice-ClassSlot Association

**Input**: Design documents from `/specs/059-remove-classslot-association/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included in every phase per Constitution Principle II (TDD is mandatory): tests are written FIRST and MUST FAIL before implementation begins. Run with `make test` (`cd backend && uv run pytest`).

**Organization**: Tasks grouped by user story to enable independent implementation and testing. The model refactor (Phase 2) is shared by all stories.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story (US1 = P1). Setup/Foundational/Polish = no story label.
- Each task includes an exact file path.

## Tech stack reference (from plan.md)

Python 3.13 / Django 5.0.14, PostgreSQL 16 (Docker), pytest, ruff, i18n via `gettext_lazy`/`{% translate %}` + `backend/locale/es/LC_MESSAGES/django.po`. Code in `backend/apps/classes/`. Tests in `backend/tests/test_classes_classprice.py`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm a green baseline and ready environment before adding the refactoring.

- [X] T001 Verify green baseline (`ruff check .` + `pytest`) in `backend/` before changes — 321 passed
- [X] T002 Start PostgreSQL and apply migrations (`make db-up` + `cd backend && uv run manage.py migrate`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update the data model layer — remove `class_slot` FK and constraint, update tests to reflect the decoupled model. **MUST complete before ANY user story.**

**⚠️ CRITICAL**: No user story work can begin until this phase is complete. Per Research Decision 1, the migration uses `RemoveField` + `RemoveConstraint`. Per Decision 5, tests are rewritten first (TDD).

- [X] T003 Write failing tests for decoupled `ClassPrice` model (no `class_slot` field, standalone `enter_price`) in `backend/tests/test_classes_classprice.py`
- [X] T004 Remove `class_slot` FK and filtered `UniqueConstraint` from `ClassPrice` model in `backend/apps/classes/models.py` (depends T003)
- [X] T005 [P] Generate migration `0004_remove_classprice_class_slot` in `backend/apps/classes/migrations/0004_remove_classprice_class_slot.py` (depends T004)
- [X] T006 [P] Update `ClassPriceAdmin` to remove `class_slot` from list_display/search_fields/readonly_fields in `backend/apps/classes/admin.py` (depends T004)

**Checkpoint**: Model decoupled — `ClassPrice` has no `class_slot`, migration generated, admin updated, tests reflect new structure.

---

## Phase 3: User Story 1 - Price Records Are Decoupled From Class Slots (Priority: P1) 🎯 MVP

**Goal**: Remove all `class_slot` references from views, forms, URLs, templates, and the schedule page so `ClassPrice` is fully standalone.

**Independent Test**: The `ClassPrice` model has no `class_slot` field. All tests pass. No reference to `class_slot` exists in ClassPrice-related code paths (models, views, forms, templates, URLs, admin). The schedule page has no "Prices" link.

- [X] T007 [P] [US1] Rewrite `enter_price` to not require `class_slot` (standalone create) in `backend/apps/classes/models.py` (depends T004, T003)
- [X] T008 [P] [US1] Rework `ClassPriceCreateView` (remove class_slot context, admin-only) in `backend/apps/classes/views.py` (depends T006, T007)
- [X] T009 [P] [US1] Rework `ClassPricesView` (global list, not per-class) in `backend/apps/classes/views.py` (depends T006)
- [X] T010 [P] [US1] Update URLs to `prices/` and `prices/add/` in `backend/apps/classes/urls.py` (depends T008, T009)
- [X] T011 [P] [US1] Rework `class_prices.html` template (remove class_slot, global listing) in `backend/apps/classes/templates/classes/class_prices.html` (depends T008, T009)
- [X] T012 [P] [US1] Rework `class_price_form.html` template (remove class_slot context) in `backend/apps/classes/templates/classes/class_price_form.html` (depends T008)
- [X] T013 [P] [US1] Remove "Prices" link from `schedule.html` in `backend/apps/classes/templates/classes/schedule.html` (depends T010)
- [X] T014 [US1] Run quickstart Scenario 1–6 validation (no class_slot anywhere, standalone pricing) (depends T007–T013) — all 34 tests pass

**Checkpoint**: All user stories complete — `ClassPrice` is fully decoupled from `ClassSlot`.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Internationalization, validation, and quality gates.

- [X] T015 [P] Compile Spanish translations in `backend/locale/` (`cd backend && uv run manage.py compilemessages -l es`)
- [X] T016 [P] Run quickstart Scenario 6 validation (i18n intact) (depends T014) — all fuzzy flags removed, Spanish strings verified
- [X] T017 Clean up dead code (`ClassSlotManager`) in `backend/apps/classes/models.py` (depends T004)
- [X] T018 Run full suite + lint + format (`make test && make lint && make format`) — 320 tests pass, format applied

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Setup. **BLOCKS** all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **Polish (Phase 4)**: Depends on User Story 1 completion.

### Within Each Phase

- Tests are written first and MUST FAIL before implementation.
- Model/service changes before the views, forms, URLs, and templates that depend on them.
- Core implementation before integration (quickstart validation) at phase end.

### Parallel Opportunities

- **Foundational**: T005 (migration), T006 (admin) touch different files and all depend only on T004 → run in parallel.
- **US1**: T007 (enter_price) and T008/T009 (views) depend on T004 but touch different methods → can run in parallel after T003.
  - T010 (URLs), T011 (prices template), T012 (form template), T013 (schedule) each touch different files → all parallel after their view/route dependencies.
- **Polish**: T015 (compile), T016 (i18n validation), T017 (cleanup) touch different files → run in parallel.

### Parallel Example: US1

```bash
# These five tasks touch independent files and can run concurrently after T007/T009:
Task: "Rework ClassPricesView (global list, not per-class) in backend/apps/classes/views.py"
Task: "Update URLs to prices/ and prices/add/ in backend/apps/classes/urls.py"
Task: "Rework class_prices.html template (remove class_slot, global listing) in backend/apps/classes/templates/classes/class_prices.html"
Task: "Rework class_price_form.html template (remove class_slot context) in backend/apps/classes/templates/classes/class_price_form.html"
Task: "Remove 'Prices' link from schedule.html in backend/apps/classes/templates/classes/schedule.html"
```

---

## Implementation Strategy

### Refactoring (single user story)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational — rewrite tests first (TDD), remove `class_slot` from model, generate migration, update admin.
3. Complete Phase 3: Rework `enter_price`, views, URLs, templates, and remove schedule link.
4. **VALIDATE**: Run all quickstart scenarios.
5. Polish — compile i18n, clean up dead code, full test + lint suite.

### Environment Reference

When writing task execution steps or running code, use these exact commands:
- **Run native dev server**: `make serve`
- **Run migrations**: `make migrate` (`cd backend && uv run manage.py migrate`)
- **Create migration (model changes)**: `cd backend && uv run manage.py makemigrations classes`
- **Compile translations**: `cd backend && uv run manage.py compilemessages`
- **Run tests**: `make test` (`cd backend && uv run pytest`)
- **Lint**: `make lint` (`cd backend && uv run ruff check .`)
- **Format**: `make format` (`cd backend && uv run ruff format .`)
- **Start database**: `make db-up`

---

## Notes

- **[P]** tasks = different files, no dependencies on incomplete tasks.
- **[US1]** labels map tasks to the single user story for traceability; Setup/Foundational/Polish carry no story label.
- Tests are included in every phase per Constitution Principle II (TDD mandatory) — write first, confirm RED, then implement.
- Commit after each logical group: `git add . && git commit -m "[Spec Kit] <phase>"`.
- Stop at any checkpoint to validate story independently.
- The `enter_price` service is reworked to create standalone current prices without per-class swap logic (per Research Decision 2).
- The filtered unique constraint `unique_current_classprice_per_slot` is removed (per Research Decision 1).
