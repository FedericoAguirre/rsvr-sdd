# Tasks: Payment Form Redesign

**Input**: Design documents from `specs/023-redesign-payment-form/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: TDD is mandatory per project constitution. Tests MUST be written and FAIL before implementation begins (Red-Green-Refactor).

**Organization**: Tasks are grouped by user story. Both stories share the same implementation code — US1 delivers the visual change, US2 verifies code consistency.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Setup (Shared Infrastructure)

*Not required — project is already initialized. No new dependencies or tools needed.*

---

## Phase 2: Foundational (Blocking Prerequisites)

*Not required — no blocking infrastructure exists. The payment form and form class already exist; changes are purely structural.*

---

## Phase 3: User Story 1 - Standardized Payment Form (Priority: P1) 🎯 MVP

**Goal**: Operators see a payment form with two-column grid layout (`col-md-6`) and consistent Bootstrap input styling (`form-control`), matching client/equipment/reservation forms.

**Independent Test**: Navigate to `/payments/create/` and visually confirm fields use `col-md-6` grid and all inputs have `form-control` styling. The two new automated tests provide programmatic verification.

### Tests for User Story 1 (TDD — Write first, expect FAIL) ⚠️

- [X] T001 [P] [US1] Write widget attrs unit test in `backend/tests/test_payments.py` — asserts every entry in `PaymentForm.Meta.widgets` has `"class": "form-control"` in its attrs. **Expected**: FAIL against current code (no widget has form-control). **Actual**: FAILED as expected — RED confirmed.
- [X] T002 [P] [US1] Write rendered HTML integration test in `backend/tests/test_payments.py` — GET `/payments/create/` and assert response contains `col-md-6` and does NOT contain `col-12` (in field wrappers). **Expected**: FAIL against current code (template uses col-12). **Actual**: FAILED — RED confirmed.

### Implementation for User Story 1

- [X] T003 [US1] Add `"class": "form-control"` to every widget in `PaymentForm.Meta.widgets` in `backend/apps/payments/forms.py`. Add widget entries for `client`, `amount`, `payment_type`, `payment_identifier`, `class_slot_count`, `reference`, and `evidence` using `Select`, `NumberInput`, `TextInput`, and `FileInput` as appropriate. Merge attrs with existing `date` (`type: date`) and `notes` (`rows: 3`). Makes T001 pass. **Actual**: PASS — GREEN.
- [X] T004 [US1] Change field wrapper class from `col-12` to `col-md-6` in `backend/apps/payments/templates/payments/payment_form.html`. Keep the button row `<div class="col-12">` unchanged. Preserve `enctype="multipart/form-data"` on the `<form>` tag. Makes T002 pass. **Actual**: PASS — GREEN.
- [X] T005 [US1] Run full test suite to confirm zero regressions: `cd backend && python -m pytest tests/test_payments.py -v`. All 14+ existing test classes plus the 2 new tests must pass. **Actual**: 27/27 PASS — GREEN.

**Checkpoint**: Payment form visually matches project standards. All tests green.

---

## Phase 4: User Story 2 - Code Consistency Verification (Priority: P2)

**Goal**: Code reviewers can confirm the payments form and template follow the same widget/column patterns as reference forms (ClientForm, EquipmentForm).

**Independent Test**: Side-by-side diff comparison of `backend/apps/payments/forms.py` with `backend/apps/clients/forms.py` and `backend/apps/payments/templates/payments/payment_form.html` with `backend/apps/equipment/templates/equipment/equipment_form.html`.

### Implementation for User Story 2

- [X] T006 [US2] Verify edit mode works: confirm locked fields (client, amount, payment_type, identifier, date, class_slot_count) have `form-control` in their `Meta.widgets` attrs. **Actual**: PASS — all 6 locked fields have `class: "form-control"` in widget defs.
- [X] T007 [US2] Verify evidence file input styling: confirm `forms.FileInput(attrs={"class": "form-control"})` is the evidence widget. Confirm `enctype="multipart/form-data"` present on `<form>`. **Actual**: PASS — both confirmed.
- [X] T008 [US2] Verify mobile responsiveness: `col-md-6` is Bootstrap responsive — 2 columns on md+ screens, stacked on small screens. **Actual**: PASS.
- [X] T009 [US2] Run i18n string scan: template uses `{% translate %}` for all user-visible text. Form labels come from model `verbose_name` (already i18n'd). Help text uses `gettext_lazy`. **Actual**: PASS — no raw strings.

**Checkpoint**: Code consistency confirmed across all reference forms. No behavioral regressions.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T010 [P] Update AGENTS.md session summary to reflect this feature (form standardization changes, TDD tests written). **Actual**: Done — session summary updated.
- [X] T011 Final visual walkthrough: confirm all code changes match project form standards (col-md-6 wrappers, form-control on all widgets, button row col-12, enctype preserved). **Actual**: PASS — verified by code review.
- [X] T012 Run full project test suite: `cd backend && python -m pytest tests/ -v` to confirm no regressions outside payments module. **Actual**: 141/144 pass — 3 pre-existing i18n failures, zero payment regressions.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A — project already initialized.
- **Foundational (Phase 2)**: N/A — no blocking infrastructure.
- **User Story 1 (Phase 3)**: Can start immediately. Tests (T001, T002) are [P] and independent of each other but block implementation (T003, T004).
- **User Story 2 (Phase 4)**: Depends on US1 implementation being complete (T003, T004). Shares the same codebase changes — verification only.
- **Polish (Phase 5)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories. This is the MVP.
- **User Story 2 (P2)**: Requires US1 implementation to be deployed (verification of the same code).

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD Red-Green-Refactor)
- Implementation before verification
- Verification before polish

### Parallel Opportunities

| Task | Parallel with | Why |
|------|---------------|-----|
| T001 | T002 | Different test methods, same file but no conflicts (different class/method names) |
| T003 | T004 | Different files (`forms.py` vs `payment_form.html`) — fully independent |
| T006 | T007 | Different verification scenarios, independent |
| T010 | T011 | Different concerns |

---

## Parallel Example: User Story 1

```bash
# Launch both tests in parallel (different classes, same file):
Task: "Write widget attrs unit test in backend/tests/test_payments.py"
Task: "Write rendered HTML integration test in backend/tests/test_payments.py"

# Launch both implementation tasks in parallel (different files):
Task: "Update PaymentForm widget attrs in backend/apps/payments/forms.py"
Task: "Update template field wrappers in backend/apps/payments/templates/payments/payment_form.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write T001 + T002 (tests that fail against current code) — **must see red**
2. Implement T003 + T004 (make tests green) — **must see green**
3. Run T005 (full regression)
4. **STOP**: MVP is done — payment form is visually consistent with project standards
5. Deploy/demo if ready

### Full Feature (US1 + US2)

1. Complete Phase 3: US1 (MVP)
2. Complete Phase 4: US2 (code consistency verification)
3. Complete Phase 5: Polish
4. All stories independently verified

### Team of One (recommended)

1. T001 + T002 (parallel — tests)
2. T003 + T004 (parallel — implementation)
3. T005 (regression)
4. T006 → T007 → T008 → T009 (sequential — verification)
5. T010 → T011 → T012 (polish)

---

## Notes

- [P] tasks = different files, no dependencies (or safe same-file parallelism with distinct class/method names)
- [Story] label maps task to specific user story for traceability
- TDD: Write T001+T002 first, confirm they FAIL, then implement T003+T004
- Commits expected after each task or logical group
- Total: 12 tasks across 3 phases (2 parallel test tasks, 2 parallel implementation tasks, 4 verification tasks, 3 polish tasks)
- MVP scope: T001–T005 (5 tasks)
