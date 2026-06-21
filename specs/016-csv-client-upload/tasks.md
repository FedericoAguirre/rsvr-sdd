---

description: "Task list for CSV client upload feature (016)"

---

# Tasks: CSV Client Upload

**Input**: Design documents from `specs/016-csv-client-upload/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/csv-format.md

**Tests**: Per constitution mandate (TDD), tests are written FIRST and must FAIL before implementation.

**Organization**: Tasks are grouped by user story. US1+US2+US3 are tightly coupled (same upload flow) and combined in Phase 3.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All source code under `backend/apps/clients/`
- Tests under `backend/tests/`
- Templates under `backend/apps/clients/templates/clients/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare existing project infrastructure for CSV upload feature

- [X] T001 Configure file upload settings (FILE_UPLOAD_MAX_MEMORY_SIZE, DATA_UPLOAD_MAX_NUMBER_FIELDS) in backend/config/settings.py

---

## Phase 2: Foundational — CSV Import Core Logic

**Purpose**: Core CSV parsing, cleansing, matching, and processing engine that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Phase 2 (TDD — write first, expect failure)

- [X] T002 [P] Write unit test for `parse_csv_file()` — validates header detection, row parsing, data cleansing (trim whitespace, normalize empty→None) in backend/tests/test_client_csv_upload.py
- [X] T003 [P] Write unit test for `match_client()` — name match (case-insensitive), email match (case-insensitive), mobile match, no-match→returns None in backend/tests/test_client_csv_upload.py
- [X] T004 [P] Write unit test for `process_csv_rows()` — correct created/updated/error counts, UNIQUE constraint handling, row-level error isolation in backend/tests/test_client_csv_upload.py

### Implementation for Phase 2

- [X] T005 [P] Implement `parse_csv_file(file) -> list[dict]` in backend/apps/clients/csv_import.py — reads CSV via DictReader, validates headers, cleanses data, returns rows list
- [X] T006 [US1] Implement `match_client(row, qs) -> Client|None` in backend/apps/clients/csv_import.py — multi-pass matching: name → email → mobile, uses `icontains`/case-insensitive queries
- [X] T007 [US1] Implement `process_csv_rows(rows) -> ImportResult` in backend/apps/clients/csv_import.py — iterates rows, calls match_client, creates/updates Clients via bulk operations, catches IntegrityError, returns ImportResult namedtuple (total, created, updated, errors, error_details)
- [X] T008 [US1] Implement `ImportResult` dataclass/namedtuple in backend/apps/clients/csv_import.py — fields: total_rows, created, updated, errors, error_details (list of {row, message})

**Checkpoint**: Core CSV import engine complete — can parse, match, and process CSV rows

---

## Phase 3: User Story 1 + 2 + 3 — Upload, Validate, Display Results (Priority: P1/P2) 🎯 MVP

**Goal**: Operator can upload a CSV, see validation errors, and view processing results

**Independent Test**: Upload a CSV with a mix of new and existing clients; verify correct created/updated/error counts in the results summary

### Tests for Phase 3 (TDD — write first, expect failure)

- [X] T009 [P] [US1] Write integration test for GET /clients/upload/ — returns 200, contains upload form with file input in backend/tests/test_client_csv_upload.py
- [X] T010 [US1] Write integration test for POST /clients/upload/ with valid CSV — returns 200, displays correct result counts (created, updated, errors) in backend/tests/test_client_csv_upload.py
- [X] T011 [US2] Write integration test for POST /clients/upload/ with missing header — returns error message, no rows processed in backend/tests/test_client_csv_upload.py
- [X] T012 [US2] Write integration test for POST /clients/upload/ with rows missing email AND mobile — row skipped, counted as error in backend/tests/test_client_csv_upload.py
- [X] T013 [US2] Write integration test for POST /clients/upload/ with empty file — returns error message in backend/tests/test_client_csv_upload.py
- [X] T014 [US3] Write integration test for POST /clients/upload/ with all-new CSV — summary shows total = n, created = n, updated = 0, errors = 0 in backend/tests/test_client_csv_upload.py

### Implementation for Phase 3

- [X] T015 [P] [US1] Add `ClientCsvUploadForm` with FileField in backend/apps/clients/forms.py — accepts .csv files, validates file size < 5MB, uses Bootstrap form-control widget
- [X] T016 [P] [US1] Add `client_csv_upload` view (GET+POST, @login_required) in backend/apps/clients/views.py — GET renders upload form, POST reads file → calls csv_import process_csv_rows → renders results in template context
- [X] T017 [P] [US1] Add `upload/` URL pattern to `urlpatterns` in backend/apps/clients/urls.py — name="client-csv-upload"
- [X] T018 [P] [US1] Create `client_csv_upload.html` template extending base.html in backend/apps/clients/templates/clients/ — upload form with file input, submit button, and download template link; conditional results section
- [X] T019 [US2] Create `_client_csv_results.html` partial template in backend/apps/clients/templates/clients/ — displays summary counts (total, created, updated, errors) with color-coded badges and error detail list
- [X] T020 [US2] Add inline file-level validation in `client_csv_upload` view in backend/apps/clients/views.py — reject empty files, check file extension is .csv, return form errors before processing
- [X] T021 [US3] Wire results context from process_csv_rows into template rendering in backend/apps/clients/views.py — pass ImportResult fields to template, show results section conditionally when processing completed
- [X] T022 [P] [US1] Add i18n `{% translate %}` / `{% blocktranslate %}` tags to both templates — all user-facing strings must use Django i18n
- [X] T023 [US1] Add Python `gettext` calls for all user-facing messages in views.py and forms.py

**Checkpoint**: At this point, US1, US2, and US3 are fully functional — Operator can upload, validate, and see results

---

## Phase 4: User Story 4 — Download CSV Template (Priority: P3)

**Goal**: Operator can download a sample CSV template with correct headers

**Independent Test**: Hit /clients/template/ and verify the response is a CSV file with headers (first_name, last_name, email, mobile) and one sample row

### Tests for Phase 4 (TDD — write first, expect failure)

- [X] T024 [P] [US4] Write integration test for GET /clients/template/ — returns 200, Content-Type text/csv, filename includes "client_template" in backend/tests/test_client_csv_upload.py
- [X] T025 [US4] Write integration test for downloaded CSV content — contains correct header row and exactly one sample data row in backend/tests/test_client_csv_upload.py

### Implementation for Phase 4

- [X] T026 [P] [US4] Add `client_csv_template` view (GET, @login_required) in backend/apps/clients/views.py — returns StreamingHttpResponse with CSV header + one sample row
- [X] T027 [US4] Add `template/` URL pattern to `urlpatterns` in backend/apps/clients/urls.py — name="client-csv-template"
- [X] T028 [P] [US4] Add download template link in `client_csv_upload.html` — visible on the upload page

**Checkpoint**: Full feature complete — upload, validate, view results, and download template

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, i18n compilation, and code quality

- [X] T029 [P] Compile translation messages: `django-admin compilemessages` in backend/
- [X] T030 Run ruff linter on all new/changed files — fix any violations
- [X] T031 Run full test suite — all tests must pass (TDD verified: tests were written first and now pass with implementation)
- [X] T032 Run quickstart validation — confirm sample CSVs process correctly via the UI

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phase 3: US1+2+3)**: Depends on Foundational core engine (`csv_import.py`)
- **User Story 4 (Phase 4)**: Independent of Phase 3 (different view) but depends on Foundational for style consistency
- **Polish (Phase 5)**: Depends on all user story phases being complete

### User Story Dependencies

- **US1+2+3 (P1/P2)**: Can start after Foundational — tightly coupled, implement together
- **US4 (P3)**: Can start after Foundational — no dependency on US1+2+3; can run in parallel

### Within Each Phase

- Tests MUST be written and FAIL before implementation (TDD per constitution)
- Core logic before views
- Views before templates
- Templates before polish

### Parallel Opportunities

- **Phase 2 tests**: T002, T003, T004 can run in parallel (different test functions, same file)
- **Phase 2 implementation**: T005, T006, T007 are sequential (each builds on previous)
- **Phase 3 tests**: T009–T014 can run in parallel after Phase 2 complete
- **Phase 3 implementation**: T015, T016, T017, T018 are parallelizable [P] (form, view, url, template are different files)
- **Phase 4**: Fully parallel with Phase 3 (different views, no shared files)
- **US4**: Can be assigned to a different developer while US1+2+3 is in progress

---

## Parallel Example: Phase 3 (US1+2+3)

```bash
# Launch all tests together (TDD):
Task: "Integration test for GET /clients/upload/ (T009)"
Task: "Integration test for POST valid CSV (T010)"
Task: "Integration test for missing header (T011)"
Task: "Integration test for missing email+mobile (T012)"
Task: "Integration test for empty file (T013)"
Task: "Integration test for all-new CSV (T014)"

# Launch parallel implementations:
Task: "Add ClientCsvUploadForm in forms.py (T015)"
Task: "Add client_csv_upload view in views.py (T016)"
Task: "Add upload/ URL pattern in urls.py (T017)"
Task: "Create client_csv_upload.html template (T018)"
```

## Parallel Example: Phase 4 (US4) + Phase 3 (US1+2+3)

```bash
# Developer A works on Phase 3:
Task: "Add ClientCsvUploadForm + view + templates (T015-T023)"

# Developer B works on Phase 4 (fully independent):
Task: "Add client_csv_template view + URL + tests (T024-T028)"
```

---

## Implementation Strategy

### MVP First (Phase 1 + 2 + 3)

1. Complete Phase 1: Setup (settings.py)
2. Complete Phase 2: csv_import.py core engine (foundational)
3. Complete Phase 3: Upload form, view, validation, results templates
4. **STOP and VALIDATE**: Upload test CSVs, verify processing, check error handling
5. Deploy/demo — MVP delivers US1, US2, US3

### Incremental Delivery

1. Phase 1 + 2 → CSV core engine ready (parsing, matching, processing)
2. Phase 3 → Full upload/validate/results flow (MVP!)
3. Phase 4 → Template download (P3 convenience feature)
4. Phase 5 → Polish, compilemessages, lint, final test run

### Parallel Team Strategy

With multiple developers:
1. Developer A: Phase 2 (csv_import.py core) + Phase 3 (upload flow)
2. Developer B: Phase 4 (template download) — starts after Phase 2 core is stable
3. Both converge for Phase 5 (polish, final test run)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Tests MUST fail before implementation (TDD per constitution)
- Commit after each logical task group
- Stop at any checkpoint to validate independently
- US1, US2, US3 are combined in Phase 3 because they share the same upload flow
- US4 (template download) is truly independent and can be parallelized
- All user-facing strings use Django i18n (Spanish)
