# Feature Specification: User Story Helper Skill

**Feature Branch**: `036-user-story-helper-skill`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "From the @ai/templates/user_story_template.md template I want to create the user-story-helper skill. So I can use markdown files to pass as specs to the /speckit.specify command."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a new user story via AI prompt (Priority: P1)

As a developer using opencode, I want to say something like "I want to create a new feature for [feature description]" and have the AI ask me clarifying questions, then save a formatted user story file.

**Why this priority**: This is the core value — turn a vague feature request into a structured user story file with minimal friction.

**Independent Test**: A developer types "I want to create a login feature" in the AI chat. The skill asks up to 3 clarifying questions (e.g., who the users are, what authentication method). After answers are provided, a file appears at `ai/features/todo/01_login_feature.md` containing the filled template.

**Acceptance Scenarios**:

1. **Given** the skill is loaded, **When** the user says "I want to create a new feature for [description]", **Then** the skill loads the template from `ai/templates/user_story_template.md`
2. **Given** the skill loaded the template, **When** the user's description is missing information (e.g., no user type, no goal), **Then** the skill asks follow-up questions (up to 3) to fill the gaps
3. **Given** the user provided all necessary information, **When** the skill processes the input, **Then** it saves a file at `ai/features/todo/[sequence]_[user_story].md` with the template filled

---

### User Story 2 - Filename follows sequence convention (Priority: P1)

As a developer, I want each user story file to have a unique, ordered filename so I can track backlog items chronologically.

**Why this priority**: Consistent naming prevents conflicts and makes backlog navigation predictable.

**Independent Test**: Create two user stories in sequence. The first file is `01_first_feature.md` and the second is `02_second_feature.md`.

**Acceptance Scenarios**:

1. **Given** no existing todo files, **When** the skill saves a user story, **Then** the filename is `01_[user_story_slug].md`
2. **Given** existing todo files with highest sequence `07`, **When** the skill saves a new user story, **Then** the filename starts with `08_`
3. **Given** user story title "Add User Authentication", **When** the skill generates the filename, **Then** the slug is `add_user_authentication` (lowercase, underscores for spaces)

---

### User Story 3 - Skill is loadable and triggerable (Priority: P2)

As a developer, I want the skill to be registered in the opencode skill system so it activates automatically when I mention feature creation phrases.

**Why this priority**: Without registration, the skill is inaccessible.

**Independent Test**: Open opencode's skill list. Confirm `user-story-helper` appears with trigger phrases listed. Say "I want to create a new feature" and confirm the skill activates.

**Acceptance Scenarios**:

1. **Given** the skill is installed at `.agents/skills/user-story-helper/SKILL.md`, **When** opencode loads skills, **Then** the skill appears in the available skills list
2. **Given** the skill is active, **When** the user says "I want to create a new feature" or "I want to create a user story" or "new feature idea", **Then** the skill activates and begins the template flow
3. **Given** the skill is active, **When** the user says unrelated phrases, **Then** the skill does not activate

---

### User Story 4 - Follow-up questions fill template gaps (Priority: P2)

As a developer, I want the skill to ask targeted questions when my initial description is incomplete, so I don't have to manually fill the template.

**Why this priority**: Follow-ups reduce cognitive load and ensure no template section is left blank.

**Independent Test**: Say "I want a feature for exporting reports". The skill asks "Who is the user type?" (e.g., admin), "What is the goal?" (e.g., export to CSV), "What is the acceptance criteria?" — then saves the completed file.

**Acceptance Scenarios**:

1. **Given** the user's description lacks a user type, **When** the skill processes it, **Then** it asks "As a [type_of_user] — who is the user for this feature?"
2. **Given** the user's description lacks a goal, **When** the skill processes it, **Then** it asks "I want [goal] — what should this feature accomplish?"
3. **Given** the user's description lacks acceptance criteria, **When** the skill processes it, **Then** it asks at least one "Given/When/Then" clarification

---

### Edge Cases

- What happens when the template file (`ai/templates/user_story_template.md`) is missing? — Skill should warn the user and abort gracefully.
- What happens when the output directory (`ai/features/todo/`) does not exist? — Skill should create it automatically.
- What happens when the user provides contradictory information in follow-up answers? — Skill should flag the contradiction and ask for confirmation.
- How does the sequence number behave when the highest existing file is `07` but `08` is already taken? — Skill should find the next available gap in the sequence.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Skill MUST load the user story template from `ai/templates/user_story_template.md` when triggered
- **FR-002**: Skill MUST detect information gaps in the user's description for at least these fields: user type, goal, reason/benefit, acceptance criteria
- **FR-003**: Skill MUST ask follow-up questions for detected gaps, up to a maximum of 3 questions per session
- **FR-004**: Skill MUST generate the filename as `[NN]_[slug].md` where `NN` is the next available 2-digit sequence and `slug` is a lowercase, underscore-separated version of the story title
- **FR-005**: Skill MUST save the filled template to `ai/features/todo/[filename]`
- **FR-006**: Skill MUST trigger on phrases including "I want to create a new feature", "I want to create a user story", "new feature idea", and similar variants
- **FR-007**: Skill MUST NOT activate on unrelated conversational phrases
- **FR-008**: Skill MUST gracefully handle the case where `ai/templates/user_story_template.md` does not exist, with a clear error message
- **FR-009**: Skill MUST create the `ai/features/todo/` directory if it does not exist
- **FR-010**: Skill MUST wrap the skill definition in the opencode-compatible SKILL.md format with YAML frontmatter including name, description (with trigger phrases), and license metadata

### Key Entities

- **User Story (markdown file)**: A structured file in `ai/features/todo/` following the user story template. Key attributes: title, user type, goal, reason, acceptance criteria, definition of done.
- **Template**: A markdown file at `ai/templates/user_story_template.md` defining the structure for new user stories.
- **Skill Definition**: A SKILL.md file at `.agents/skills/user-story-helper/SKILL.md` with YAML frontmatter and trigger phrase configuration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can go from "I want to create a new feature" to a saved `ai/features/todo/[NN]_[slug].md` file in under 3 minutes (including follow-up questions)
- **SC-002**: The skill saves a file with all template sections filled (no blank sections) at least 90% of the time
- **SC-003**: The sequence number in the filename correctly increments by 1 from the highest existing todo file
- **SC-004**: The skill activates correctly for each of the specified trigger phrases and does not activate for unrelated phrases (verified via test conversation)

## Assumptions

- The user has opencode installed and skill auto-detection is enabled
- The template file at `ai/templates/user_story_template.md` already exists with the current structure
- The skill follows the existing SKILL.md format convention used by other skills in `.agents/skills/`
- The 2-digit sequence numbering (01–99) is sufficient for the project's todo backlog
- The user is comfortable answering up to 3 clarifying questions in the same conversation turn
- Different AI models (deepseek, gpt, claude) may produce slightly different content quality — the skill format and trigger logic should be model-agnostic
