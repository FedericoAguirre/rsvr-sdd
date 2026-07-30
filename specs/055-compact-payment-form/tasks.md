---

description: "Task list for compact payment form layout feature"

---

# Tasks: Compact Payment Form Layout for Single-Screen View

**Input**: Design documents from `specs/055-compact-payment-form/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/README.md

**Tests**: Not included — spec does not request new tests; existing payment tests must continue to pass.

**Organization**: Tasks map user stories to sequential modifications of the single template file `backend/apps/payments/templates/payments/payment_form.html`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/apps/payments/templates/payments/payment_form.html`
- All changes are in the single template file plus its embedded `<style>` block.

---

## Phase 1: Setup

**Purpose**: Review current template and confirm pre-existing test baseline

- [X] T001 Read the current `payment_form.html` at `backend/apps/payments/templates/payments/payment_form.html` to understand the existing fieldset structure, CSS classes, and i18n patterns
- [X] T002 Run existing payment tests to establish baseline: `cd backend && uv run pytest tests/test_payments*.py -v --tb=short`

---

## Phase 2: Foundational

**Purpose**: No foundational tasks — no shared infrastructure needed. All changes are isolated to a single template file.

---

## Phase 3: User Story 1 - Create Payment Without Scrolling (Priority: P1) 🎯 MVP

**Goal**: Staff users can create a payment on `/payments/create/` with all fields and buttons visible in a single 1080p viewport without scrolling.

**Independent Test**: Open `/payments/create/` on a 1080p display; verify no vertical scrollbar appears and all fieldsets + buttons are visible.

### Implementation for User Story 1

- [X] T003 [P] [US1] Compact title: Change `<h2 class="mb-4">` to `<h4 class="mb-2">` in create mode section of `backend/apps/payments/templates/payments/payment_form.html`
- [X] T004 [P] [US1] Compact fieldset spacing: Change fieldset margins from `mb-4` to `mb-2` in all three create-mode fieldsets in `backend/apps/payments/templates/payments/payment_form.html`
- [X] T005 [P] [US1] Compact field margins: Change all field wrapper divs from `mb-3` to `mb-2` in create mode sections of `backend/apps/payments/templates/payments/payment_form.html`
- [X] T006 [US1] Re-layout Date+Notes as side-by-side: Wrap date and notes fields in a `div.row.g-2` with `col-md-6` each in the Context fieldset of `backend/apps/payments/templates/payments/payment_form.html` (currently notes is below date; change to side-by-side row)
- [X] T007 [US1] Re-layout Documentation section to 3-column: Change payment_identifier, reference, and evidence from current layout (2-col + full-width) to a single `div.row.g-2` with three `col-md-4` columns in `backend/apps/payments/templates/payments/payment_form.html`
- [X] T008 [P] [US1] Add compact CSS: Replace or extend the `<style>` block in `backend/apps/payments/templates/payments/payment_form.html` with compact styling: `.form-label-compact` (0.9rem, lighter margin), `.payment-form fieldset` (reduced padding/margin, bottom border only), `.form-help-collapsed` (hidden by default, shown on focus via CSS), `.form-actions` (compact spacing, top border only), responsive media queries for tablet/mobile
- [X] T009 [US1] Add help text toggle JavaScript: Add a `<script>` block in `backend/apps/payments/templates/payments/payment_form.html` that shows help text on field focus and hides on blur (if field empty)
- [X] T010 [US1] Compact buttons: Change button container from current layout to `.form-actions` with `btn-sm` classes on submit and cancel buttons in `backend/apps/payments/templates/payments/payment_form.html`
- [X] T011 [US1] Verify create mode fits desktop: Open `/payments/create/` on 1080p display; confirm no vertical scrollbar; check all fields visible; check form submission still works

**Checkpoint**: Create mode is fully compact and functional

---

## Phase 4: User Story 2 - Edit Payment With Compact Layout (Priority: P2)

**Goal**: Staff users editing an existing payment see the same compact layout as create mode.

**Independent Test**: Open the edit page for an existing payment; verify all fields fit without scrolling; save changes successfully.

### Implementation for User Story 2

- [X] T012 [P] [US2] Compact edit mode loop: Apply compact spacing (`mb-2` instead of `mb-3`) to the `{% for field in form %}` loop in the edit mode (`{% else %}`) branch of `backend/apps/payments/templates/payments/payment_form.html`
- [X] T013 [P] [US2] Compact edit mode button area: Apply `.btn-sm` and `.form-actions` styling to the edit mode button row in `backend/apps/payments/templates/payments/payment_form.html`
- [X] T014 [US2] Verify edit mode: Open an existing payment's edit page on 1080p display; confirm no scrollbar; save changes successfully

**Checkpoint**: Both create and edit modes are compact and functional

---

## Phase 5: User Story 3 - Responsive Behavior on Smaller Screens (Priority: P3)

**Goal**: The form remains usable on tablet and mobile viewports with stacked layout and no horizontal overflow.

**Independent Test**: Resize browser to 768px then 375px; verify fields stack vertically, buttons become full-width, and no horizontal scrolling occurs.

### Implementation for User Story 3

- [X] T015 [US3] Add mobile responsive CSS: Add `@media (max-width: 768px)` block in the `<style>` section of `backend/apps/payments/templates/payments/payment_form.html` with mobile adjustments: stacked action buttons (full-width), reduced font sizes, tighter fieldset padding, and no horizontal overflow
- [X] T016 [US3] Add tablet responsive CSS: Add `@media (min-width: 769px) and (max-width: 1024px)` block in the `<style>` section of `backend/apps/payments/templates/payments/payment_form.html` with tablet adjustments: slightly increased row gaps for readability
- [X] T017 [US3] Verify responsive breakpoints: Resize browser to 768px — confirm vertical stacking; resize to 375px — confirm no horizontal scroll; test at 1024px — confirm intermediate adjustments apply

**Checkpoint**: Responsive behavior works at all breakpoints

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T018 [P] Run full payment test suite: `cd backend && uv run pytest tests/test_payments*.py -v --tb=short` — 109 passed, 1 pre-existing failure (test_empty_payment_shows_message)
- [X] T019 Verify i18n compliance: Scan the modified template for any hardcoded user-visible strings; all labels, buttons, and help text must use `{% translate %}` or `{% blocktrans %}`
- [X] T020 Run quickstart validation: Follow the validation scenarios in `specs/055-compact-payment-form/quickstart.md` — desktop fit, help text interaction, multi-column layouts, responsive breakpoints, form submission, edit mode

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **US1 (Phase 3)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US2 (Phase 4)**: Depends on US1 completion (edit mode builds on template changes from create mode)
- **US3 (Phase 5)**: Depends on US2 completion (responsive CSS adjustments rely on final fieldset structure)
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Can start after Setup — No dependencies on other stories
- **US2 (P2)**: Depends on US1 — same template file must have create mode layout first
- **US3 (P3)**: Depends on US2 — responsive styles adjust the final layout

### Within Each User Story

- Implementation tasks within a story can mostly run in parallel (marked [P])
- Verify checkpoint at end of each story before proceeding

### Parallel Opportunities

- All tasks marked [P] within a story can run in parallel (they modify different lines/sections of the same file)
- Phase 6 polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all independent file edits together:
Task: "T003 Compact title — change h2 to h4"
Task: "T004 Compact fieldset spacing — mb-4 to mb-2"
Task: "T005 Compact field margins — mb-3 to mb-2"
Task: "T008 Add compact CSS and responsive base styles"

# Then sequential tasks (same file, interdependent):
Task: "T006 Re-layout Date+Notes as side-by-side"
Task: "T007 Re-layout Documentation to 3-column"
Task: "T009 Add help text toggle JavaScript"
Task: "T010 Compact buttons with btn-sm"

# Verify:
Task: "T011 Manual verification on 1080p display"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (review template, run baseline tests)
2. Complete Phase 3: US1 — Create mode compact layout
3. **STOP and VALIDATE**: Create mode fits 1080p viewport
4. Deliver as MVP

### Incremental Delivery

1. **US1 (P1)**: Create mode compact → Test → Deploy (MVP)
2. **US2 (P2)**: Edit mode compact → Test → Deploy
3. **US3 (P3)**: Responsive adjustments → Test → Deploy

### Environment Reference

- **Run tests**: `cd backend && uv run pytest apps/payments/tests/`
- **Run single test**: `cd backend && uv run pytest apps/payments/tests/ -k test_name`
- **Run dev server**: `cd backend && uv run manage.py runserver`
- **Run migrations**: `cd backend && uv run manage.py migrate`

---

## Notes

- All changes are confined to `backend/apps/payments/templates/payments/payment_form.html` — no backend Python changes needed
- [P] tasks = different sections of the same file that can be edited independently (no overlapping line ranges)
- [Story] label maps task to specific user story for traceability
- Each user story should be independently verifiable after its checkpoint
- Commit after each task or logical group
- Verify existing tests pass after each phase
