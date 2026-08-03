# Tasks: Class Price Versioning & Audit

**Input**: Design documents from `/specs/058-class-prices/` (plan.md, spec.md, research.md, data-model.md, contracts/README.md, quickstart.md)

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included in every phase per Constitution Principle II (TDD is mandatory): tests are written FIRST and MUST FAIL before implementation begins. Run with `make test` (`cd backend && uv run pytest`).

**Organization**: Tasks grouped by user story (US1/US2/US3) to enable independent implementation and testing. Foundational model (Phase 2) is shared by all stories.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story (US1 = P1, US2 = P2, US3 = P3). Setup/Foundational/Polish = no story label.
- Each task includes an exact file path.

## Tech stack reference (from plan.md)

Python 3.13 / Django 5.0.14, PostgreSQL 16 (Docker), pytest, ruff, i18n via `gettext_lazy`/`{% translate %}` + `backend/locale/es/LC_MESSAGES/django.po`. New code in `backend/apps/classes/`. Tests in `backend/tests/test_classes_classprice.py`.

---

## Phase 1: Setup

**Purpose**: Confirm a green baseline and ready environment before adding the feature.

- [ ] T001 Verify green baseline (`ruff check .` + `pytest`) in `backend/` before changes
- [ ] T002 Start PostgreSQL and apply migrations (`make db-up` + `cd backend && uv run manage.py migrate`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The `ClassPrice` data model and its integrity invariants. **MUST complete before ANY user story.**

**⚠️ CRITICAL**: No user story work can begin until this phase is complete. Per Research Decision 1, `ClassPrice` references `ClassSlot` (the project's "class" entity — no separate `Class` model exists). Per Decision 2, the single-current constraint uses a Django filtered `UniqueConstraint`; per Decision 5, attribution uses `created_by`/`changed_by` FKs (cf. `Payment`).

- [ ] T003 Write failing tests for `ClassPrice` model invariants (fields, single-current via filtered constraint, attribution) in `backend/tests/test_classes_classprice.py`
- [ ] T004 Create `ClassPrice` model (class_slot FK, price, current, created_by, created_at, changed_at, changed_by, updated_at) + filtered `UniqueConstraint` in `backend/apps/classes/models.py` (depends T003)
- [ ] T005 [P] Generate migration for `ClassPrice` in `backend/apps/classes/migrations/0003_classprice.py` (depends T004)
- [ ] T006 [P] Register `ClassPrice` in Django admin in `backend/apps/classes/admin.py` (depends T004)
- [ ] T007 [P] Add `ClassPrice` + audit i18n strings in `backend/locale/es/LC_MESSAGES/django.po` (depends T004)

**Checkpoint**: Foundation ready — `ClassPrice` model, migration, admin, and i18n in place.

---

## Phase 3: User Story 1 — Enter/Update a Class Price with History (Priority: P1) 🎯 MVP

**Goal**: An administrator enters a new price; the prior current price is archived (`current=False`, `changed_at`, `changed_by`) and a new current price is created, all within one atomic transaction. (SC-001, SC-003, SC-006)

**Independent Test**: Enter two prices for a class; verify the first is inactive with a changer recorded, the second is current, only one current exists, and a failure rolls back leaving the previous price current.

- [ ] T008 [US1] Write failing tests for the atomic price-swap service in `backend/tests/test_classes_classprice.py`
- [ ] T009 [US1] Implement atomic price-entry service (`transaction.atomic` + `select_for_update`) in `backend/apps/classes/models.py` (depends T004, T008)
- [ ] T010 [US1] Create `ClassPriceForm` in `backend/apps/classes/forms.py` (depends T009)
- [ ] T011 [US1] Implement `ClassPriceCreateView` (admin-only) in `backend/apps/classes/views.py` (depends T010)
- [ ] T012 [P] [US1] Add POST route `classes/<int:pk>/prices/add/` in `backend/apps/classes/urls.py` (depends T011)
- [ ] T013 [P] [US1] Add i18n strings for add-price UI in `backend/locale/es/LC_MESSAGES/django.po` (depends T011)
- [ ] T014 [US1] Run quickstart Scenario 1–2 validation (enter price, atomic swap) (depends T011)

**Checkpoint**: User Story 1 complete — price entry works with full history preservation.

---

## Phase 4: User Story 2 — Review Complete Price History (Priority: P2)

**Goal**: An administrator views all price records for a class in descending order with the active price clearly flagged. (FR-006, FR-007, SC-002)

**Independent Test**: Re-price a class three times; open the prices page; verify descending order, the "Current" badge on the active record, and audit attribution (creator/changer) on every row, plus an empty state when no prices exist.

- [ ] T015 [US2] Write failing tests for `ClassPricesView` (ordering, current flag, empty state) in `backend/tests/test_classes_classprice.py`
- [ ] T016 [US2] Implement `ClassPricesView` (current price + history queryset, descending) in `backend/apps/classes/views.py` (depends T004, T015)
- [ ] T017 [P] [US2] Create `class_prices.html` template in `backend/apps/classes/templates/classes/class_prices.html` (depends T016)
- [ ] T018 [P] [US2] Add GET route `classes/<int:pk>/prices/` in `backend/apps/classes/urls.py` (depends T016)
- [ ] T019 [P] [US2] Add "Prices" link to schedule per slot in `backend/apps/classes/templates/classes/schedule.html` (depends T016)
- [ ] T020 [P] [US2] Add i18n strings for prices-view UI in `backend/locale/es/LC_MESSAGES/django.po` (depends T016)
- [ ] T021 [US2] Run quickstart Scenario 4 validation (history ordering, current flag, empty state) (depends T016, T017, T018)

**Checkpoint**: User Stories 1 AND 2 both functional independently.

---

## Phase 5: User Story 3 — Prevent Deletion (Priority: P3)

**Goal**: No `ClassPrice` record (current or historical) can be deleted via the ORM, queryset, or admin. (FR-008, SC-005)

**Independent Test**: Attempt to delete a current and a historical price via instance `.delete()`, bulk `QuerySet.delete()`, and the admin delete action; verify every attempt is refused with a clear message and zero records are removed.

- [ ] T022 [US3] Write failing tests for deletion prevention (instance + queryset + admin) in `backend/tests/test_classes_classprice.py`
- [ ] T023 [US3] Override `ClassPrice.delete()` and queryset `delete()` to raise in `backend/apps/classes/models.py` (depends T004, T022)
- [ ] T024 [US3] Disable delete in `ClassPriceAdmin.has_delete_permission` in `backend/apps/classes/admin.py` (depends T023)
- [ ] T025 [US3] Run quickstart Scenario 4 (deletion prevention) validation (depends T022, T023, T024)

**Checkpoint**: All user stories independently functional; price records are non-deletable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Internationalize, validate end-to-end, and confirm quality gates.

- [ ] T026 [P] Compile Spanish translations in `backend/locale/` (`cd backend && uv run manage.py compilemessages`)
- [ ] T027 Run quickstart Scenario 5 validation (admin-only restriction: non-admin denied) (depends T011)
- [ ] T028 Run full suite + lint + format (`make test && make lint && make format`)
- [ ] T029 [P] Generate Mermaid ER diagram (optional) via `/speckit.data-model-diagram.generate`
- [ ] T030 Final i18n audit: confirm all new strings have Spanish translations in `backend/locale/es/LC_MESSAGES/django.po`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Setup. **BLOCKS** all user stories.
- **User Stories (Phase 3–5)**: All depend on Foundational completion.
  - User Story 1 (P1) — no dependencies on US2/US3.
  - User Story 2 (P2) — no dependencies on US1/US3 (shares the foundational model only).
  - User Story 3 (P3) — no dependencies on US1/US2 (adds the deletion guard to the model).
- **Polish (Phase 6)**: Depends on all user stories being complete.

### Within Each User Story

- Tests are written first and MUST FAIL before implementation.
- Model/service before the view, form, and routes that depend on it.
- Core implementation before integration (quickstart validation) at story end.

### Parallel Opportunities

- **Foundational**: T005 (migration), T006 (admin), T007 (i18n) touch different files and all depend only on T004 → run in parallel.
- **US1**: T012 (route) and T013 (i18n) touch different files and depend only on T011/T010 respectively → run in parallel.
- **US2**: T017 (template), T018 (route), T019 (schedule link), T020 (i18n) touch different files, all depend only on T016 → run in parallel.
- **Polish**: T026 (compile), T029 (diagram), T030 (i18n audit) are independent concerns → run in parallel.
- Different user stories can be built in parallel by different developers once Foundational is complete.

### Parallel Example: User Story 2

```bash
# These four tasks touch independent files and can run concurrently:
Task: "Create class_prices.html template in backend/apps/classes/templates/classes/class_prices.html"
Task: "Add GET route classes/<int:pk>/prices/ in backend/apps/classes/urls.py"
Task: "Add 'Prices' link to schedule per slot in backend/apps/classes/templates/classes/schedule.html"
Task: "Add i18n strings for prices-view UI in backend/locale/es/LC_MESSAGES/django.po"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories).
3. Complete Phase 3: User Story 1 → an administrator can enter a versioned price.
4. **STOP and VALIDATE**: Run US1 quickstart Scenario 1–2 independently.

> Note: Per the template's typical guidance the MVP is US1 alone. However, the user's stated need is to *see* the last price — so US2 (the prices view) is recommended alongside US1 for the first usable increment; enter US1+US2 together, then US3, then polish.

### Incremental Delivery

1. Setup + Foundational → Foundation ready.
2. US1 → Test independently → Deploy/Demo (MVP!).
3. US2 → Test independently → Deploy/Demo (now prices are visible).
4. US3 → Test independently → Deploy/Demo (deletion-safe).
5. Polish → full i18n verification + regression.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together.
2. Once Foundational is done, the three stories can be built in parallel:
   - Developer A: User Story 1 (price entry)
   - Developer B: User Story 2 (price history view)
   - Developer C: User Story 3 (deletion prevention)
3. Each story completes and integrates independently against the shared model.

---

## Environment Reference

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
- **[Story]** labels map tasks to specific user stories for traceability; Setup/Foundational/Polish carry no story label.
- Tests are included in every phase per Constitution Principle II (TDD mandatory) — write first, confirm RED, then implement.
- Commit after each logical group: `git add . && git commit -m "[Spec Kit] <phase>"`.
- Stop at any checkpoint to validate a story independently.
