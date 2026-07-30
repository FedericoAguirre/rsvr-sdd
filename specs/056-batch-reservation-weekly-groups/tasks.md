# Tasks: Batch Reservation Weekly Date Groups

**Input**: Design documents from `specs/056-batch-reservation-weekly-groups/`

**Prerequisites**: plan.md, spec.md (required), research.md, data-model.md, contracts/README.md

**Tests**: No explicit test tasks — existing `test_payments_batch.py` covers backend data/submission; visual layout is verified via quickstart scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/payments/templates/payments/`
- **Tests**: `backend/tests/`
- **Locale**: `backend/locale/es/LC_MESSAGES/`

---

## Phase 1: Setup

**Purpose**: Understand current implementation and establish baseline

- [X] T001 Read `backend/apps/payments/templates/payments/payment_detail.html` and `backend/apps/payments/templates/payments/_batch_modal.html` to understand existing JS rendering (`renderBatchForm`, `DAY_ABBRS`, `toggleDate`), CSS structure, and i18n patterns
- [X] T002 Run existing batch tests to establish baseline: `cd backend && uv run pytest tests/test_payments_batch.py -v --tb=short`

---

## Phase 2: Foundational (Infrastructure)

**Purpose**: Set up CSS grid classes, modal scrolling, and i18n bridge for day abbreviations

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Add embedded `<style>` block in `backend/apps/payments/templates/payments/payment_detail.html` with CSS grid classes: `.batch-date-grid`, `.week-group`, `.week-header`, `.day-label`, `.week-row`, `.week-separator`, responsive media query for <768px
- [X] T004 Add `modal-dialog-scrollable` class in `backend/apps/payments/templates/payments/_batch_modal.html` (change `class="modal-dialog modal-lg"` to `class="modal-dialog modal-dialog-scrollable modal-lg"`)
- [X] T005 Pass day abbreviations from Django template to JS: added `<script id="dayAbbrs" type="application/json">` with `{% translate %}` for each abbreviation, replaced `var DAY_ABBRS = ["L", "M", "X", "J", "V", "S", "D"];` with `JSON.parse(...)`

**Checkpoint**: CSS grid classes are ready, modal scrolls, day abbreviations pass through i18n

---

## Phase 3: User Story 1 — View Dates Grouped by Week (Priority: P1) 🎯 MVP

**Goal**: Staff users see 20 dates arranged in 4 weekly rows with day-of-week column headers (Lun, Mar, Mié, Jue, Vie) instead of a single flex-wrap row.

**Independent Test**: Open `/payments/{id}/?batch_modal=1` on a 1080p display and confirm dates appear in 4 rows × 5 columns with day headers labeled Lun–Vie.

### Implementation for User Story 1

- [X] T006 [US1] Modify `renderBatchForm()` to group dates by week: collect valid dates into array, slice into groups of 5, render `.week-group` > `.week-header` (5 day labels) + `.week-row` (5 date buttons), insert `.week-separator` between groups
- [X] T007 [US1] Change button format from `DAY_ABBRS[pyDow] + ' - ' + d.replace(/-/g, "/")` to short `DD/M` format via `parseInt(parts[2]) + '/' + parseInt(parts[1])`

**Checkpoint**: Weekly grid renders correctly with 4 rows of 5 columns and day headers. Date selection still works.

---

## Phase 4: User Story 2 — Select Dates from Weekly Grid (Priority: P2)

**Goal**: Clicking date buttons toggles selection with visual feedback and real-time count update — identical to current behavior but in the new grid layout.

**Independent Test**: Click 3 date buttons in different weeks — each toggles active state (blue/outline). Selection count updates to 3. Confirm button is disabled when empty.

### Implementation for User Story 2

- [X] T008 [US2] Verify `toggleDate()` function works correctly with the new `.week-row` grid structure — `data-date` and `data-dow` attributes preserved, `onclick="toggleDate(this)"` unchanged, button classes (btn-primary/btn-outline-secondary) identical

**Checkpoint**: Date selection works identically to the current implementation

---

## Phase 5: User Story 3 — Use Modal on Smaller Screens (Priority: P3)

**Goal**: The weekly grid remains usable on tablet and mobile viewports without horizontal overflow.

**Independent Test**: Resize browser to 768px and 375px widths — 5-column grid preserved, no horizontal scroll, modal body scrolls vertically if needed.

### Implementation for User Story 3

- [X] T009 [US3] Add responsive CSS within the `<style>` block in `backend/apps/payments/templates/payments/payment_detail.html` — `@media (max-width: 768px)` and `@media (max-width: 480px)` breakpoints added

**Checkpoint**: Modal is usable at all viewport widths without horizontal overflow

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: i18n compliance, locale updates, validation

- [X] T010 Add day abbreviation translations (Lun, Mar, Mié, Jue, Vie, Sáb, Dom) to `backend/locale/es/LC_MESSAGES/django.po` and run `compilemessages` — 247 translated messages
- [X] T011 [P] Remove unused `batchData` variable and `filterDatesBySlot()` no-op function from `payment_detail.html`
- [X] T012 Run full batch test suite to confirm no regressions: `cd backend && uv run pytest tests/test_payments_batch.py -v --tb=short` — 11/11 passed; full suite 109/110 (1 pre-existing failure)
- [X] T013 Run quickstart validation: Django system check passes (0 errors), tests 11/11, expanded suite 109/110 (1 pre-existing)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — **BLOCKS all user stories**
- **User Stories (Phase 3–5)**: Depend on Foundational
  - US1 (P1) — must complete first (grid layout)
  - US2 (P2) — depends on US1 (selection on grid)
  - US3 (P3) — depends on US1 (responsive for grid)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **US1 (P1)**: Must complete first — the grid layout is the foundation
- **US2 (P2)**: Depends on US1 — selection operates on the new grid HTML
- **US3 (P3)**: Depends on US1 — responsive CSS adjusts the grid

### Within Each Phase

- [P] tasks within the same phase can run in parallel (different files)
- Core implementation before verification

### Parallel Opportunities

- T003 (CSS) and T004 (modal-dialog-scrollable) can run in parallel
- T011 (remove dead code) can run in parallel with T012 (tests)

---

## Parallel Example: Foundational Phase

```bash
# Run CSS grid styles + modal scrolling changes in parallel:
Task: "T003 Add CSS grid classes in payment_detail.html <style> block"
Task: "T004 Add modal-dialog-scrollable in _batch_modal.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (read template, baseline tests)
2. Complete Phase 2: Foundational (CSS, scroll, i18n bridge)
3. Complete Phase 3: User Story 1 (weekly grid layout)
4. **STOP and VALIDATE**: Open batch modal on 1080p — 4 rows × 5 columns with Lun–Vie headers
5. Deploy/demo if ready

### Incremental Delivery

1. Phase 1 + Phase 2 → Infrastructure ready
2. Add US1 (weekly grid) → **MVP — deployable!**
3. Add US2 (selection verification) → confirm interaction unchanged
4. Add US3 (responsive CSS) → mobile-friendly
5. Phase 6 → i18n, tests, polish

### Environment Reference

- **Run tests**: `cd backend && uv run pytest tests/test_payments_batch.py -v --tb=short`
- **Run server**: `cd backend && uv run manage.py runserver`
- **Compile messages**: `cd backend && uv run manage.py compilemessages`
