# Tasks: RSVR Sales Demonstration Script

**Input**: Design documents from `specs/057-sales-demonstration-script/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No test tasks included — this is a documentation-only feature; no application code changes, so no unit/integration/contract tests apply. Validation is performed via the manual scenarios in `quickstart.md`.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different document sections, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Deliverable: `docs/sales_script.md` (repository root `docs/`)
- All other application paths under `backend/` are **read-only sources** — never modified
- All tasks operate on the single deliverable document unless noted otherwise

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare repository state and gather source-of-truth material for the document

^- [x] T001 Verify working tree on branch `057-sales-demonstration-script` and existing suite passes (`make test`, `make lint`) before any doc work
^- [x] T002 Confirm `docs/sales_script.md` does not already exist (or capture existing content to reconcile if it does)
^- [x] T003 Collect authoritative feature inventory: read `backend/config/urls.py` and each app's `urls.py` and `views.py` (clients, reservations, classes, equipment, payments)
^- [x] T004 [P] Collect business-rule sources: read `backend/apps/*/models.py` (constraints, `clean()`, choices) and relevant forms
^- [x] T005 [P] Collect navigation and Spanish UI labels: read `backend/templates/base.html` and `backend/locale/es/LC_MESSAGES/django.po`
^- [x] T006 [P] Reconcile existing docs: read `docs/windows11_deployment.md` and `README.md` to confirm they contain no demo-feature content conflicting with implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the document skeleton and contract-compliant structure that ALL user stories build on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

^- [x] T007 Create `docs/sales_script.md` with the 10 required top-level sections per `contracts/sales-script-contract.md` (Purpose/Audience; Demonstration Preparation; Recommended Demonstration Flow; Feature Catalog; Business Rules; Feature Status and Known Gaps; FAQ; New Feature Request Questionnaire; Feature Request Handoff; Maintenance and Verification)
^- [x] T008 Add header block to `docs/sales_script.md`: feature name, purpose, audience, and how the script relates to the actual application (source-of-truth statement)
^- [x] T009 Add the demonstration preparation content to `docs/sales_script.md` (Section 2): account setup, `make seed` demo data, environment/prereqs, and how to reach the app
^- [x] T010 [P] Write the FAQ template and New Feature Request Questionnaire scaffolding (Sections 7–8) so the structure exists for US2/US3 to fill

**Checkpoint**: Document skeleton ready — user story implementation can now begin.

---

## Phase 3: User Story 1 - Demonstrate the Application to a Prospective User (Priority: P1) 🎯 MVP

**Goal**: Deliver the core demonstration capability — a logical demo flow over the implemented features with accurate business rules, so a demonstrator can present the app consistently and without over-promising.

**Independent Test**: Follow the Recommended Demonstration Flow in `docs/sales_script.md` against a seeded running instance; every documented step must produce the documented expected result, and no unimplemented feature may be presented as available (quickstart Scenarios 3, 5).

### Implementation for User Story 1

^- [x] T011 [US1] Write Section 1 (Purpose and Audience) and the Application Overview subsection (3.1) of `docs/sales_script.md`
^- [x] T012 [US1] Write the Authentication and User Access subsection (3.2) of `docs/sales_script.md` (login/logout, admin, session-based access)
^- [x] T013 [US1] Write the Main Navigation subsection (3.3) of `docs/sales_script.md` matching the `base.html` menu order (Clients → Payments → Reservations → Equipment → Schedule → Reports → Admin)
^- [x] T014 [US1] Write the Core Business Workflow subsection (3.4) of `docs/sales_script.md` covering the reservation lifecycle (create with auto-date, duplicate prevention, status transitions reserved/used/unused)
^- [x] T015 [US1] Write the Data Management subsection (3.5) of `docs/sales_script.md` covering clients (search/create/CSV upload) and equipment (list/create/edit/status)
^- [x] T016 [US1] Write the Reporting and Visualization subsection (3.6) of `docs/sales_script.md` covering payment reports (superuser-only), charts, and PDF/CSV exports
^- [x] T017 [US1] Write the Administration subsection (3.7) and Other Implemented Features subsection (3.8) of `docs/sales_script.md` (admin site, class schedule toggling)
^- [x] T018 [US1] Write the Feature Catalog (Section 4) of `docs/sales_script.md` as a table with columns Feature / Status / User-Role / Demonstration Location / Business Area, populated from the T003 route/view inventory (quickstart Scenario 2)
^- [x] T019 [US1] Write the Business Rules section (Section 5) of `docs/sales_script.md` grounded in the T004 model/validation sources (client contact rule, reservation uniqueness, equipment/class-slot PROTECT limitation, payment identifier uniqueness, soft-delete lifecycle, superuser report access) (quickstart Scenario 3)
^- [x] T020 [US1] Write the Feature Status and Known Gaps section (Section 6) of `docs/sales_script.md` using the status vocabulary (`Implemented`, `Partially implemented`, `Known limitation`, `Not implemented`, `Future feature`) per `contracts/sales-script-contract.md`, ensuring no unsupported claims (quickstart Scenario 2)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently — a demonstrator can run a complete, accurate demonstration.

---

## Phase 4: User Story 2 - Locate Feature Information During a Demonstration (Priority: P2)

**Goal**: Provide quick lookup and answers for ad-hoc questions during a live demonstration, without interrupting the flow.

**Independent Test**: Ask a question about any cataloged feature and confirm the status and demonstration location are locatable in under 1 minute via the catalog and FAQ (quickstart Scenario 4).

### Implementation for User Story 2

^- [x] T021 [P] [US2] Write the Frequently Asked Feature Questions section (Section 7) of `docs/sales_script.md` — each entry: question, concise answer, status, and a reference to the relevant section (derived from implemented capabilities per research Decision 3)
^- [x] T022 [P] [US2] Verify the Feature Catalog (Section 4) is complete and searchable: every implemented feature has a status, user/role, and demonstration location; empty/inapplicable sections are removed (quickstart Scenario 4)
^- [x] T023 [US2] Cross-check FAQ answers against the application behavior (views/models) to ensure no FAQ answer conflicts with the source-of-truth rule

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Capture a New Feature Request (Priority: P2)

**Goal**: Enable capture of prospective-user feature requests during or after a sales conversation and hand off structured, spec-ready input to development.

**Independent Test**: Complete the questionnaire for a hypothetical feature request and confirm the handoff template can be used as initial input for a Spec Kit specification (quickstart Scenario 6).

### Implementation for User Story 3

^- [x] T024 [US3] Write the New Feature Request Questionnaire (Section 8) of `docs/sales_script.md` covering all 12 mandatory questions per `contracts/sales-script-contract.md`
^- [x] T025 [US3] Write the Feature Request Handoff template (Section 9) of `docs/sales_script.md` with the 16 Spec-Kit-aligned fields (Feature Name, Requester, User Role, Business Problem, Business Goal, User Need, Expected Behavior, Business Rules, Data Requirements, Acceptance Criteria, Examples, Priority, Required Date, Related RSVR Features, Open Questions, Development Notes)
^- [x] T026 [US3] Add guidance to Section 9 of `docs/sales_script.md` converting a captured questionnaire into development-ready requirements (per spec AC-09)

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect the whole document

^- [x] T027 Write the Maintenance and Verification section (Section 10) of `docs/sales_script.md` describing how to update features, business rules, statuses, and demo steps as the app evolves (spec AC-11)
^- [x] T028 [P] Review the document for business-oriented, scannable language; remove any empty/inapplicable sections (spec AC-03, quality requirements)
^- [x] T029 [P] Run `make test` and `make lint` to confirm no application regression from the documentation-only change
^- [x] T030 Run the full `quickstart.md` validation scenarios (1–7) and confirm all checkboxes pass; document any failures
^- [x] T031 If the feature originated from an `ai/features/todos/` file, move `ai/features/todos/27_sales_script.md` to `ai/features/done/` and append any follow-up requests per the constitution workflow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on the Feature Catalog created in US1 (T018) but is independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Document sections flow top-down: flow → catalog → business rules → status → FAQ → questionnaire → handoff
- Core demonstration content (US1) before lookup (US2) before capture (US3)

### Parallel Opportunities

- T004, T005, T006 (Setup) run in parallel — independent source reads
- T021, T022 (US2) can run in parallel — different sections
- US1 and US3 sections could be drafted in parallel by different writers since they touch different sections of `docs/sales_script.md`

---

## Parallel Example: User Story 1

```bash
# Launch section-writing tasks that touch different parts of docs/sales_script.md together:
Task: "Write Core Business Workflow subsection (3.4) of docs/sales_script.md"
Task: "Write Data Management subsection (3.5) of docs/sales_script.md"
Task: "Write Reporting and Visualization subsection (3.6) of docs/sales_script.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently (quickstart Scenarios 3, 5)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Environment Reference

When validating the document against the running app, use these exact commands:
- **Start environment**: `make db-up && make migrate && make seed && make serve`
- **Run tests**: `make test`
- **Run lint**: `make lint`

---

## Notes

- [P] tasks = different files/sections, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Do NOT modify anything under `backend/` — application code is source-of-truth reference only
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same-section conflicts, cross-story dependencies that break independence
