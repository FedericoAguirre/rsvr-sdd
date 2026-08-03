# Tasks: Price Format Display

**Input**: Design documents from `/specs/063-price-format/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Included per Constitution Principle II (Testing Standards — NON-NEGOTIABLE). TDD: write tests first, verify they FAIL, then implement.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- Django monolith: `backend/` at repository root
- Tests: `backend/tests/` (pytest + Django test client)
- Templates: `backend/apps/<app>/templates/<app>/`

---

## Phase 1: Setup

**Purpose**: No setup required — project infrastructure already exists, `currency` filter already in `payment_extras.py`, all dependencies installed.

*No tasks for this phase.*

---

## Phase 2: Foundational

**Purpose**: No new foundational work needed. The `currency` template filter in `backend/apps/payments/templatetags/payment_extras.py` already provides the exact format (`$N,NNN.NN` via `f"${float(value):,.2f}"`). No new models, apps, or configuration.

*No tasks for this phase.*

---

## Phase 3: User Story 1 - Formatted Price Display (Priority: P1) 🎯 MVP

**Goal**: Apply `$N,NNN.NN` formatting to all price amounts on the class prices page (current prices alert + history table).

**Independent Test**: Navigate to `/classes/prices/` and verify every price is displayed as `$N,NNN.NN`. Raw decimal values without formatting confirm the fix is needed.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST per Constitution Principle II (TDD). Ensure they FAIL before implementation.**

- [x] T001 [P] [US1] Add test for formatted `$` prefix and thousand separators in price display in `backend/tests/test_classes_classprice.py`
- [x] T002 [P] [US1] Add test for two-decimal-place formatting (e.g., `50` becomes `$50.00`) in `backend/tests/test_classes_classprice.py`

### Implementation for User Story 1

- [x] T003 [US1] Add `{% load payment_extras %}` alongside existing `{% load i18n %}` in `backend/apps/classes/templates/classes/class_prices.html`
- [x] T004 [P] [US1] Apply `|currency` filter to `{{ price.price }}` in "Current prices" alert section in `backend/apps/classes/templates/classes/class_prices.html`
- [x] T005 [P] [US1] Apply `|currency` filter to `{{ price.price }}` in price history table in `backend/apps/classes/templates/classes/class_prices.html`
- [x] T006 [US1] Run full test suite and verify all existing tests still pass

**Checkpoint**: At this point, all prices on the class prices page render as `$N,NNN.NN`. Raw `Decimal` output is eliminated.

---

## Phase 4: User Story 2 - Form Consistency (Priority: P2)

**Goal**: Verify the price input form remains functional and newly-entered prices appear formatted on the subsequent page load.

**Independent Test**: Enter a price via the form, submit, and verify the resulting page displays the new price formatted as `$N,NNN.NN`.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST per Constitution Principle II (TDD). Ensure they FAIL before implementation (or verify they pass if no changes are needed).**

- [x] T007 [US2] Add end-to-end test for form entry + formatted display in `backend/tests/test_classes_classprice.py`

### Implementation for User Story 2

- [x] T008 [US2] Verify `backend/apps/classes/templates/classes/class_price_form.html` input field has `step="0.01"` for decimal entry — confirm no changes needed
- [x] T009 [US2] Run full test suite and verify form submission + formatted display loop passes

**Checkpoint**: Both viewing and entering prices work correctly with formatted display.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup.

- [x] T010 Run quickstart.md validation scenarios: verify current prices alert, history table, form entry, and edge cases
- [x] T011 Run `make docker-build && make docker-up` to validate Docker stack with template changes
- [x] T012 [P] Scan all touched files for raw user-visible strings per Constitution III (i18n) — confirm no new untranslated strings introduced

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A — no tasks
- **Foundational (Phase 2)**: N/A — no tasks
- **User Story 1 (Phase 3)**: No dependencies — can start immediately
- **User Story 2 (Phase 4)**: Depends on US1 completion (tests the formatted output from US1)
- **Polish (Phase 5)**: Depends on US1 + US2 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies — can start immediately
- **User Story 2 (P2)**: Depends on US1 (validates the format introduced in US1)

### Within Each User Story

- Tests (T001, T002) MUST be written and FAIL before implementation (T003-T006)
- Template changes (T004, T005) can run in parallel
- T003 must run before T004, T005 (load tag must be added first)

### Parallel Opportunities

- T001 and T002 (US1 tests) can run in parallel
- T004 and T005 (US1 template changes) can run in parallel
- All tasks within a single file (`class_prices.html`) are NOT parallelizable with each other

---

## Parallel Example: User Story 1

```bash
# Step 1: Launch both tests together (TDD — verify FAIL):
Task: "Add test for formatted $ prefix and thousand separators in backend/tests/test_classes_classprice.py"
Task: "Add test for two-decimal-place formatting in backend/tests/test_classes_classprice.py"

# Step 2: After tests fail, implement template changes:
Task: "Add {% load payment_extras %} in backend/apps/classes/templates/classes/class_prices.html"
# Then in parallel:
Task: "Apply |currency filter to Current prices alert in class_prices.html"
Task: "Apply |currency filter to history table in class_prices.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write tests T001, T002 → verify they FAIL (no formatting yet)
2. Implement T003 (add `{% load %}` tag)
3. Implement T004, T005 (apply `|currency` filter in both locations)
4. Run tests T006 → verify all pass + existing tests pass
5. **STOP and VALIDATE**: Visit `/classes/prices/` — prices show as `$N,NNN.NN`
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Phase 3: User Story 1 → Test independently → Deploy/Demo (MVP!)
2. Complete Phase 4: User Story 2 → Test independently → Deploy/Demo
3. Complete Phase 5: Polish → Final validation → Ready for merge

### Environment Reference

- **Run tests**: `uv run manage.py test` (local) or `docker compose exec web uv run manage.py test` (Docker)
- **Run migrations**: `docker compose exec web uv run manage.py migrate`
- **Build + deploy**: `make docker-build && make docker-up`

---

## Notes

- [P] tasks = different files or independent sections, no dependencies
- [Story] label maps task to specific user story for traceability
- TDD per Constitution II: tests MUST be written and fail before implementation
- The `currency` filter at `backend/apps/payments/templatetags/payment_extras.py:19-27` already produces `$N,NNN.NN` — no changes needed to the filter itself
- No data model changes — `ClassPrice.price` remains `DecimalField(10,2)`
- No i18n entries needed — numeric formatting only, no new translated strings
- Commit after each task or logical group
