---

description: "Task list for reordering payment form fields for improved UX"

---

# Tasks: Reorder Payment Form Fields for Improved UX

**Input**: Design documents from `/specs/054-payments-form-reorder/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No new test tasks — this feature modifies form field order and template layout only. Existing form submission tests must pass unchanged.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No project initialization needed — repository already exists.

No tasks.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites — this feature modifies existing files only.

No tasks.

---

## Phase 3: User Story 1 - Enter a Payment with Logical Field Flow (Priority: P1) 🎯 MVP

**Goal**: Payment form fields on `/payments/create/` follow a logical top-to-bottom order: Cliente, Amount, Cantidad de bloques de clase, Tipo de pago, Fecha, Notas, Identificador de pago, Referencia, Comprobante, then submit/cancel buttons.

**Independent Test**: Navigate to `/payments/create/` and verify fields appear in the exact order specified above. Tab through the form to confirm tab order matches visual order.

### Implementation for User Story 1

- [X] T001 [P] [US1] Reorder fields in `Meta.fields` list in `payments/forms.py` to match the new display order: client, amount, class_slot_count, payment_type, date, notes, payment_identifier, reference, evidence
- [X] T002 [US1] Update `templates/payments/payment_form.html` to render fields explicitly in the new order, grouped into logical sections (Transaction Data → Context → Documentation and Reference → Actions) with responsive Bootstrap 5 layout (Amount + class_slot_count side-by-side on desktop, payment_identifier + reference side-by-side on desktop, all fields stacked vertically on mobile)

**Checkpoint**: Payment creation form displays fields in correct order on all screen sizes

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification

- [X] T003 Navigate to `/payments/create/`, fill all required fields, submit, and verify payment is created successfully
- [X] T004 Verify responsive layout at desktop (>1024px) and mobile (<768px) widths — fields stacked correctly, no overlap, buttons aligned
- [X] T005 Verify tab order follows visual field order by pressing Tab through the entire form
- [X] T006 Verify all validation errors display below the correct field by submitting an empty form

---

## Dependencies & Execution Order

### Phase Dependencies

- **US1 (Phase 3)**: No dependencies — can start immediately
- **Polish (Phase 4)**: Depends on US1 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories

### Within Each User Story

- Form logic before template layout (T001 before T002)

### Parallel Opportunities

- T001 and T002 are marked [P] — can run in parallel (different files: `forms.py` vs `create.html`)

---

## Parallel Example: User Story 1

```bash
# Both files can be edited simultaneously:
Task: "Reorder Meta.fields in payments/forms.py"
Task: "Reorder field rendering in templates/payments/create.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 3: US1 (T001 + T002) → form reordered
2. **STOP and VALIDATE**: Navigate to `/payments/create/`, confirm field order
3. Deploy/demo if ready

### Incremental Delivery

1. Add US1 (form order + template) → Complete feature
2. Add Polish (verification) → Validated

### Environment Reference

- **Run server**: `make serve`
- **Run tests**: `make test`

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to User Story 1
- No new files needed — only `payments/forms.py` and `templates/payments/create.html` are modified
- No database migrations, no model changes, no view logic changes
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
