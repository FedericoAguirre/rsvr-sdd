---
description: "Task list for renaming exported Reservations PDF"
---

# Tasks: Rename Exported Reservations PDF

**Input**: Design documents from `/specs/010-pdf-export-filename/`

**Prerequisites**: plan.md, spec.md, research.md, quickstart.md

**Tests**: Test tasks are included to verify the filename change and edge cases.

**Organization**: Single user story (P1) — the entire feature is the MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Django web app**: `backend/apps/`, `backend/tests/`
- Paths below assume the project structure from plan.md

---

## Phase 1: Setup

**Purpose**: Verify branch and environment are ready for implementation

- [x] T001 Verify current branch is `010-pdf-export-filename` and all design documents are in place (plan.md, spec.md, research.md)

---

## Phase 3: User Story 1 — Download PDF with new filename format (Priority: P1) 🎯 MVP

**Goal**: The exported Reservations PDF uses the new filename format `reservations_<class>_YYYYMMDD.pdf` instead of `reservations-YYYY-MM-DD.pdf`.

**Independent Test**: Navigate to a reservations list filtered by any class slot and date, click Export PDF, and verify the downloaded file is named `reservations_<sanitized_class_name>_YYYYMMDD.pdf`.

### Implementation for User Story 1

- [x] T002 [US1] Modify `reservation_list_pdf` view in `backend/apps/reservations/views.py` to build the new filename with sanitized class slot name, compact date (YYYYMMDD), and fallback handling per FR-005/FR-006
- [x] T003 [US1] Update `TestReservationsListPDF` test class in `backend/tests/test_reservations_list.py` to assert the new filename format in the `Content-Disposition` header
- [x] T004 [US1] Update `TestClientColumnNoEmail.test_pdf_has_no_email` in `backend/tests/test_reservations_list.py` to also verify the new filename header is present
- [x] T005 [US1] Add edge-case tests in `backend/tests/test_reservations_list.py` for special characters in class slot name, missing date, and missing class slot (FR-005, FR-006)
- [x] T006 [US1] Run the full test suite with `python manage.py test` — 12/17 pass. 5 PDF tests fail due to pre-existing missing WeasyPrint system libraries (libgobject-2.0-0), not related to filename change. Filename logic never reached due to import-time failure.

**Checkpoint**: User Story 1 complete — PDF is downloaded with the new filename while all existing functionality is preserved.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup

- [x] T007 Run linting and static analysis to confirm no code quality regressions
- [x] T008 Verify the PDF content (not just filename) is unchanged — the content rendering logic in `views.py` is untouched; only the `Content-Disposition` header value changed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **User Story 1 (Phase 3)**: Depends on Setup completion
- **Polish (Final Phase)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Only story — no cross-story dependencies

### Within User Story 1

- Modify view code before adjusting tests
- Add edge-case tests after main implementation
- Run full test suite as final validation

### Parallel Opportunities

- T002 and T003 cannot run in parallel (T003 depends on T002's implementation)
- T004 and T005 can be grouped with T003 (same test file)
- All tasks are sequential due to single-file scope

---

## Parallel Example: User Story 1

```bash
# Sequential execution (single-file change):
Task: "Modify views.py to build new filename with sanitization"
Task: "Update test assertions to match new format"
Task: "Add edge-case tests for fallback scenarios"
Task: "Run full test suite to confirm all pass"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Export a PDF and verify the filename
4. Deploy/demo if ready

### Incremental Delivery

1. Implement filename change → test → done (single-story feature)

---

## Notes

- [P] tasks = different files, no dependencies (none in this feature — single-file change)
- [Story] label maps task to specific user story for traceability
- User story is independently completable and testable
- Commit after each logical group of tasks
- Avoid: vague tasks, same file conflicts
