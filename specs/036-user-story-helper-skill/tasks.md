---

description: "Task list for user-story-helper skill implementation"
---

# Tasks: User Story Helper Skill

**Input**: Design documents from `/specs/036-user-story-helper-skill/`

**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Not requested — acceptance verified via opencode conversation (skill is an opencode SKILL.md configuration file, not executable code).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm existing project structure is in place.

- [X] T001 Verify `ai/templates/user_story_template.md` exists and is readable
- [X] T002 Verify `.agents/skills/` directory convention (7 existing skills already present)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core setup that MUST exist before the skill can function.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 Confirm `ai/features/todo/` directory exists (create if missing)

**Checkpoint**: Foundation ready — skill implementation can begin.

---

## Phase 3: User Story 1 - Create a new user story via AI prompt (Priority: P1) 🎯 MVP

**Goal**: Skill loads the template, detects gaps in user's description, asks clarifying questions, and saves a filled user story file.

**Independent Test**: User says "I want to create a login feature" → skill asks up to 3 clarifying questions → a file appears at `ai/features/todo/01_login_feature.md` with the template filled.

### Implementation for User Story 1

- [X] T004 [P] [US1] Write SKILL.md frontmatter with name `user-story-helper`, capability summary, and trigger phrases: "I want to create a new feature", "I want to create a user story", "new feature idea"
- [X] T005 [P] [US1] In SKILL.md, add instruction: load template from `ai/templates/user_story_template.md` when triggered
- [X] T006 [US1] In SKILL.md, add instruction: detect missing template fields (user_type, goal, reason, acceptance_criteria, definition_of_done) from user input
- [X] T007 [US1] In SKILL.md, add instruction: ask up to 3 targeted follow-up questions for detected gaps
- [X] T008 [US1] In SKILL.md, add instruction: fill template sections with user answers
- [X] T009 [US1] In SKILL.md, add instruction: perform soft validation — warn if required template sections are blank but still save
- [X] T010 [US1] In SKILL.md, add instruction: save filled template to `ai/features/todo/[NN]_[slug].md`

**Checkpoint**: User Story 1 is complete — a user can go from trigger phrase to saved file with filled template.

---

## Phase 4: User Story 2 - Filename follows sequence convention (Priority: P1)

**Goal**: Each user story file gets a unique, sequentially numbered filename with proper slug transformation.

**Independent Test**: Create two user stories in sequence → first file is `01_[slug].md`, second is `02_[slug].md`.

### Implementation for User Story 2

- [X] T011 [P] [US2] In SKILL.md, add instruction: scan `ai/features/todo/` for existing files to determine next available 2-digit sequence number
- [X] T012 [P] [US2] In SKILL.md, add instruction: generate filename as `[NN]_[slug].md` where `NN` is next available sequence and `slug` is lowercase underscore-separated title
- [X] T013 [US2] In SKILL.md, add instruction: handle gap collisions — if `08` is taken, find the next available gap
- [X] T014 [US2] In SKILL.md, add instruction: slugify title — lowercase, spaces to underscores, remove special characters

**Checkpoint**: User Stories 1 AND 2 are complete — sequence numbering works correctly.

---

## Phase 5: User Story 3 - Skill is loadable and triggerable (Priority: P2)

**Goal**: Skill activates on specified trigger phrases and does NOT activate on unrelated conversation.

**Independent Test**: Open opencode's skill list → confirm `user-story-helper` appears. Say trigger phrases and confirm activation. Say unrelated phrases and confirm no activation.

### Implementation for User Story 3

- [X] T015 [P] [US3] In SKILL.md, add instruction for trigger phrase matching: exact/fuzzy match for "I want to create a new feature", "I want to create a user story", "new feature idea" and similar variants
- [X] T016 [US3] In SKILL.md, add instruction: do not activate on unrelated conversational phrases (negative matching patterns)
- [X] T017 [US3] In SKILL.md, add instruction: confirm skill path is `.agents/skills/user-story-helper/SKILL.md` following the 7 existing skills convention

**Checkpoint**: All three user stories should now be independently functional.

---

## Phase 6: User Story 4 - Follow-up questions fill template gaps (Priority: P2)

**Goal**: Skill asks targeted questions when initial description is incomplete.

**Independent Test**: Say "I want a feature for exporting reports" → skill asks "Who is the user type?" then "What is the goal?" then "What is the acceptance criteria?" → saves completed file.

### Implementation for User Story 4

- [X] T018 [P] [US4] In SKILL.md, add instruction: prioritize follow-up questions by missing field importance (user_type first, then goal, then reason, then acceptance_criteria)
- [X] T019 [P] [US4] In SKILL.md, add instruction: format follow-up questions with the template field syntax (e.g., "As a [type_of_user] — who is the user for this feature?")
- [X] T020 [US4] In SKILL.md, add instruction: handle contradictory information in follow-up answers — flag contradiction and ask for confirmation
- [X] T021 [US4] In SKILL.md, add instruction: limit to maximum 3 follow-up questions per session

**Checkpoint**: All user stories are complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, error handling, and final review.

- [X] T022 Handle missing template file: skill warns the user and aborts gracefully if `ai/templates/user_story_template.md` is missing
- [X] T023 Handle missing output directory: skill creates `ai/features/todo/` automatically if it does not exist
- [X] T024 Handle duplicate filename: when generated filename already exists, present three options — (A) overwrite, (B) use next available sequence, (C) cancel
- [X] T025 Handle write errors: catch permission denied / disk full and display clear OS-level error message to user
- [X] T026 [P] Review SKILL.md against spec requirements (FR-001 through FR-011) for completeness
- [X] T027 [P] Review SKILL.md against quickstart.md for usage accuracy consistency

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — blocks all user stories
- **User Stories (Phase 3–6)**: All depend on Foundational phase completion; stories can proceed sequentially in priority order (P1 → P2)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — core skill creation, no dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational — filename logic, independent of US1 but same phase
- **User Story 3 (P2)**: Can start after US1 + US2 — builds on skill foundation for activation logic
- **User Story 4 (P2)**: Can start after US1 + US2 — refines follow-up question logic

### Within Each User Story

- Frontmatter and structure before detailed instructions
- Core logic before edge cases
- Story complete before moving to next priority

---

## Parallel Opportunities

- All Phase 1 and Phase 2 tasks are independent of each other
- Within US1: Tasks T004–T005 (frontmatter/template loading) can be parallel with T001–T003 verification
- Within US2: T011–T013 (sequence/slug logic) can be parallel — different sections of SKILL.md
- Within US4: T018–T019 (question prioritization/formatting) can be parallel — different instruction blocks
- Polish tasks T026 and T027 can be parallel reviews

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (core flow: trigger → load template → detect gaps → ask → save)
4. Complete Phase 4: User Story 2 (filename sequence logic)
5. **STOP and VALIDATE**: Test skill end-to-end with a trigger phrase
6. Commit and verify file saved to `ai/features/todo/`

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 → Core flow works → Commit
3. US2 → Sequence numbering works → Commit
4. US3 → Trigger/activation works → Commit
5. US4 → Follow-up questions refined → Commit
6. Phase 7: Polish and edge cases → Final commit

### Environment Reference

This project is an opencode skill (pure SKILL.md configuration file). No external tools, migrations, or build steps required.

---

## Notes

- Each task corresponds to a specific section or instruction block within `.agents/skills/user-story-helper/SKILL.md`
- All tasks are about writing instructions for the AI agent, not executable code
- Validation (T026–T027) ensures spec compliance and consistency with quickstart.md
