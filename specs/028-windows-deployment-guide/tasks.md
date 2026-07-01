# Tasks: Windows Deployment Guide

**Input**: Design documents from `/specs/028-windows-deployment-guide/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Not applicable — documentation-only feature.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Files Touched

```text
README.md                        # Edit — add link to deployment guide
docs/windows11_deployment.md    # Create — deployment instructions
```

## Phase 1: Setup

**Purpose**: Understand project structure and determine what to document

- [X] T001 Investigate project configuration: WSGI module name, settings structure, requirements.txt, and existing .env template at project root

---

## Phase 2: Foundational

*Skipped* — no foundational code dependencies for a documentation-only feature.

---

## Phase 3: User Story 1 — Install and Deploy on Fresh Windows 11 Laptop (Priority: P1) 🎯 MVP

**Goal**: Write the deployment guide so a person unfamiliar with the system can go from a clean Windows 11 Home laptop to a running web application.

**Independent Test**: A person unfamiliar with the system can follow the instructions end-to-end on a clean Windows 11 Home machine and confirm the web application is accessible in a browser.

### Implementation for User Story 1

- [X] T002 [P] [US1] Write prerequisites and security configuration sections in docs/windows11_deployment.md (software checklist, admin rights, internet, Windows Defender, UAC)
- [X] T003 [P] [US1] Write RDBMS installation section in docs/windows11_deployment.md (PostgreSQL via EDB installer, service verification)
- [X] T004 [P] [US1] Write Python runtime installation section in docs/windows11_deployment.md (Python 3.12+ from python.org, PATH configuration)
- [X] T005 [P] [US1] Write project setup section in docs/windows11_deployment.md (clone repo, create .env with DATABASE_URL/SECRET_KEY/MEDIA_ROOT/ALLOWED_HOSTS/DEBUG, pip install)
- [X] T006 [P] [US1] Write database initialization section in docs/windows11_deployment.md (create database, run migrations, verify connection)
- [X] T007 [P] [US1] Write file uploads and firewall configuration sections in docs/windows11_deployment.md (media directory, netsh firewall rule)
- [X] T008 [US1] Write running the app and verification sections in docs/windows11_deployment.md (Waitress command, browser test)
- [X] T009 [US1] Write troubleshooting section and add external links in docs/windows11_deployment.md (common errors, official download/reference links)

**Checkpoint**: Full deployment guide written — a user can install and run the app from scratch using only docs/windows11_deployment.md

---

## Phase 4: User Story 2 — Restart After System Reboot (Priority: P2)

**Goal**: Add post-reboot recovery instructions so the administrator can restore the web app after a Windows restart.

**Independent Test**: The administrator can reboot the laptop and bring the web application back online using only the restart section of docs/windows11_deployment.md.

### Implementation for User Story 2

- [X] T010 [P] [US2] Write post-reboot startup section in docs/windows11_deployment.md (Windows Task Scheduler setup for auto-start on boot)
- [X] T011 [US2] Write launcher script section in docs/windows11_deployment.md (manual restart using .bat/.ps1 script, verifying no re-installation needed)

**Checkpoint**: Post-reboot recovery documented — a user can restart the app after Windows reboot without repeating installation.

---

## Phase 5: User Story 3 — Discover Guide from README (Priority: P3)

**Goal**: Add a link in README.md so users can find and navigate to the Windows deployment guide.

**Independent Test**: A user can find the Windows deployment link in README.md and open docs/windows11_deployment.md.

### Implementation for User Story 3

- [X] T012 [US3] Add link to docs/windows11_deployment.md in README.md

**Checkpoint**: README.md contains a visible link to the deployment guide — single-click navigation works.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, file organization, and completion of workflow requirements.

- [X] T013 Review docs/windows11_deployment.md for consistency, accuracy, and completeness against spec requirements FR-001 through FR-010
- [X] T014 Move the feature todo file ai/features/todos/01-deployment-script-windows.md to ai/features/done/ as per constitution workflow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — can start immediately
- **Phase 2 (Foundational)**: Skipped
- **Phase 3 (US1 - P1)**: Depends on Phase 1 completion
- **Phase 4 (US2 - P2)**: Depends on Phase 3 — adds content to same file (docs/windows11_deployment.md)
- **Phase 5 (US3 - P3)**: Can start after Phase 3 — modifies README.md only, no dependency on Phase 4
- **Phase 6 (Polish)**: Depends on all phases complete

### User Story Dependencies

- **US1 (P1)**: Can start after Setup — no dependencies on other stories
- **US2 (P2)**: Must follow US1 — adds content to the same deployment guide file
- **US3 (P3)**: Can start after US1 — modifies README.md independently

### Parallel Opportunities

- All US1 content tasks (T002 through T007) marked [P] can be written in parallel as independent sections
- T008 (running the app) depends on all prior US1 sections
- T009 (troubleshooting + links) depends on T002–T008 being complete
- T010 and T011 [US2] are sequential within that phase
- T012 [US3] is independent of US2 — can run in parallel with Phase 4

---

## Parallel Example: User Story 1

```bash
# Launch all US1 section writing tasks in parallel:
Task: "Write prerequisites and security sections in docs/windows11_deployment.md"
Task: "Write RDBMS installation section in docs/windows11_deployment.md"
Task: "Write Python runtime section in docs/windows11_deployment.md"
Task: "Write project setup section in docs/windows11_deployment.md"
Task: "Write database initialization section in docs/windows11_deployment.md"
Task: "Write file uploads and firewall sections in docs/windows11_deployment.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1 (full deployment guide)
3. **STOP and VALIDATE**: Can a user follow the guide end-to-end?
4. Ship the deployment guide as MVP

### Incremental Delivery

1. Phase 1 + Phase 3 → MVP: deployment guide is usable
2. Add Phase 4 (US2) → post-reboot recovery documented
3. Add Phase 5 (US3) → README link added for discoverability
4. Each story adds value without invalidating previous work

### Parallel Delivery

- One writer can draft US1 sections in parallel
- US3 (README link) is a trivial change that can be done at any time after US1
