# Tasks: Replace WeasyPrint with ReportLab for Cross-Platform PDF

**Input**: Design documents from `/specs/038-replace-weasyprint-pdf/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks included per TDD requirement (constitution — non-negotiable). Tests MUST be written and reviewed BEFORE implementation, and MUST fail initially.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` for Django project

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Update project dependencies and Docker configuration

- [x] T001 Update project dependencies: remove `weasyprint`, add `reportlab>=4.0` and `pdfminer.six` (for test assertions) in `backend/pyproject.toml`
- [x] T002 [P] Remove WeasyPrint system library packages (libpango-1.0-0, libpangoft2-1.0-0, libpangocairo-1.0-0, libcairo2, libgdk-pixbuf-2.0-0) from `backend/Dockerfile`

---

## Phase 2: Tests (TDD — Write Before Implementation)

**Purpose**: Update existing PDF tests to validate ReportLab output and add content-assertion tests. Tests MUST fail initially (no implementation yet).

- [x] T003 [US3] Update `test_pdf_download_content_type` and `test_pdf_empty_list` in `backend/tests/test_reservations_list.py` to assert response headers (content-type, filename) — these remain unchanged regardless of PDF engine
- [x] T004 [P] [US3] Update `test_status_in_pdf_export` in `backend/tests/test_reservations_list.py` to render the view (not the HTML template) and assert status display in PDF content using `pdfminer.six` text extraction
- [x] T005 [P] [US3] Write `test_pdf_content_contains_reservation_data` in `backend/tests/test_reservations_list.py` that renders the PDF view and asserts equipment name, client name, and class slot appear in extracted PDF text
- [x] T006 [P] [US3] Write `test_pdf_empty_state_shows_no_reservations_message` in `backend/tests/test_reservations_list.py` that renders the PDF view with no reservations and asserts the empty-state message appears in extracted PDF text
- [x] T007 [P] [US3] Add `pdfminer.six` as dev dependency in `backend/pyproject.toml` for PDF text extraction in tests

**Checkpoint**: All test tasks written. They should fail (or be skipped) since the ReportLab implementation is not yet in place. User reviews tests before proceeding.

---

## Phase 3: User Story 1 - Developer Sets Up Project on Any OS (Priority: P1) 🎯 MVP

**Goal**: Developers can install dependencies and generate PDFs on macOS, Linux, and Windows without system-level packages

### Implementation for User Story 1

- [x] T008 [US1] Implement ReportLab PDF generation using `platypus` (`SimpleDocTemplate`, `Table`, `TableStyle`, `Paragraph`) in `backend/apps/reservations/views.py` view `reservation_list_pdf`: create A4 document with title "Reservations by Class", date/class header, and three-column table (Equipment, Client, Status) with grey header row and cell borders
- [x] T009 [US1] Use Django `gettext()` for all user-visible PDF strings: title, column headers, empty-state message — matching existing i18n keys from the HTML template in `backend/apps/reservations/views.py`
- [x] T010 [US1] Wire the ReportLab output to `HttpResponse` with `Content-Type: application/pdf` and the existing filename format in `backend/apps/reservations/views.py`

---

## Phase 4: User Story 2 - User Downloads Reservation PDF (Priority: P1)

**Goal**: User clicks "Export PDF" and downloads a PDF with all reservation data and correct empty-state handling

- [x] T011 [US2] Handle empty reservation state in PDF: show class slot header and "No reservations found for this class and date." message (translated via i18n) instead of an empty table in `backend/apps/reservations/views.py`
- [x] T012 [US2] Preserve existing error handling: on PDF generation failure, log the error, set a user-friendly message via Django messages, and redirect to the reservations list in `backend/apps/reservations/views.py`
- [x] T013 [US2] Verify non-ASCII characters (ñ, accents) render correctly in PDF using ReportLab built-in fonts (Helvetica) with Latin-1 encoding — no special configuration needed per research

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup and validation

- [x] T014 Remove abandoned HTML template at `backend/apps/reservations/templates/reservations/reservation_list_pdf.html` (no longer needed — ReportLab is programmatic, not template-based)
- [x] T015 Run the full test suite to verify no regressions — 35/36 pass in reservations tests (1 pre-existing i18n assertion mismatch unrelated to PDF changes)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Tests (Phase 2)**: Depends on Setup completion — must complete before implementation (TDD)
- **User Stories (Phase 3-4)**: Depend on Phase 2 (tests must be written first)
- **Polish (Phase 5)**: Depends on all user story phases being complete

### User Story Dependencies

- **US1 (P1) + US2 (P1)**: Same code change (view implementation). US1 focuses on the core PDF generation and i18n; US2 adds edge case handling (empty state, error handling, non-ASCII)
- **US3 (P2)**: Tests — must be written before US1/US2 but pass after implementation

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Core implementation before edge cases
- Story complete before moving to polish

### Parallel Opportunities

- T002 [P] can run alongside T001
- T004-T007 [P] can all run in parallel (different test methods)
- T003 must run before parallel test tasks (it sets up the test infrastructure pattern)

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Tests (write all test tasks)
3. Complete Phase 3: US1 (core PDF generation + i18n)
4. **STOP and VALIDATE**: Tests should now pass
5. Complete Phase 4: US2 (edge cases)
6. Complete Phase 5: Polish

### Incremental Delivery

1. Setup + Tests → Foundation ready
2. Add US1 (core PDF) → Test independently → Deploy (MVP!)
3. Add US2 (edge cases) → Test independently → Deploy
4. Polish → Final validation → Deploy

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Tests use `pdfminer.six` for PDF text extraction assertions (add to dev dependencies)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Use `docker compose exec web uv run manage.py test backend.tests.test_reservations_list -k pdf` to run just PDF tests during development
