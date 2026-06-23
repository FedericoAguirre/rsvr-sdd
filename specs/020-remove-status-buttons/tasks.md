---

description: "Task list for removing inline status buttons from reservation list views"

---

# Tasks: Remove Status Buttons from Reservation List

**Input**: Design documents from `specs/020-remove-status-buttons/`

**Prerequisites**: plan.md, spec.md, research.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

---

## Phase 1: User Story 1 - Remove Inline Status Buttons (Priority: P1) 🎯 MVP

**Goal**: Remove "Used" and "Unused" inline buttons from all reservation list views while preserving status badges and detail-page functionality.

**Independent Test**: Load the reservation list page and confirm no "Used" or "Unused" buttons appear in any row; status badges are still visible.

### Implementation

- [X] T001 [P] [US1] Remove inline Used/Unused buttons from `backend/apps/reservations/templates/reservations/reservation_list.html` (keep status badge `<span>`)
- [X] T002 [P] [US1] Remove inline Used/Unused buttons from `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html` (keep status badge `<span>`)
- [X] T003 [P] [US1] Remove inline Used/Unused buttons from `backend/apps/reservations/templates/reservations/partials/reservation_row.html` (keep status badge `<span>`)

### Test Updates

- [X] T004 [US1] Update tests in `backend/tests/test_reservations_list.py` — remove assertions that check for inline Used/Unused button presence; verify all tests still pass

**Checkpoint**: Reservation list views show status badges without inline action buttons. Detail page's status forms remain functional.

---

## Phase 2: Polish & Verification

- [X] T005 Run the full test suite: `cd backend && uv run python -m pytest tests/ --reuse-db -k "not PDF and not test_clear_filters_button_exists"`
- [ ] T006 Commit and push changes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (US1)**: Can start immediately — no setup or foundational tasks needed
- **Phase 2 (Polish)**: Depends on Phase 1 completion

### User Story Dependencies

- Single user story (P1) — no other stories to depend on

### Parallel Opportunities

- T001, T002, T003 can all run in parallel (different template files, no overlap)
- T004 must run after T001–T003 (tests verify the deletion)

---

## Parallel Example: User Story 1

```bash
# Launch all template edits together:
Task: "Remove buttons from reservation_list.html"
Task: "Remove buttons from reservation_list_by_slot.html"
Task: "Remove buttons from reservation_row.html"
```

---

## Implementation Strategy

### MVP (Phase 1 Only)

1. Complete all three template edits in parallel
2. Update tests
3. Run test suite to verify
4. Deploy

### Incremental Delivery

Single increment — the entire feature is one atomic change. No staging needed.

---

## Notes

- [P] tasks can run in parallel (different files, no dependencies)
- The `reservation_change_status` view and `/status/` route are preserved for the detail page
- Status badges (`status_badge_class` / `status_label` filters) are preserved
- The CSRF fix in `base.html` (JS cookie handler) is unaffected
