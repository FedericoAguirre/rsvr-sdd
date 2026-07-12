---
name: user-story-helper
description: Create structured user story markdown files from feature descriptions. Use when the user says "I want to create a new feature", "I want to create a user story", "new feature idea", or similar phrases about creating a feature or user story for a backlog. Triggers the template-based flow: loads template, detects gaps, asks up to 3 follow-up questions, saves filled file to ai/features/todos/[NN]_[slug].md.
license: Complete terms in LICENSE.txt
---

This skill guides creation of structured user story markdown files following the project's user story template. It converts a user's feature description into a filled template file in the project's todos directory.

## Workflow

### 1. Activation

Trigger on user phrases including:
- "I want to create a new feature" (or "I want to create a new feature for...")
- "I want to create a user story"
- "new feature idea"
- Similar variants expressing intent to create a new feature/user story

Do NOT activate on unrelated conversational phrases.

### 2. Load template

Load the user story template from `ai/templates/user_story_template.md`.

If the template file does not exist:
- Warn the user: "The user story template at `ai/templates/user_story_template.md` was not found. Cannot create a user story."
- Abort the flow.

### 3. Parse user input and detect gaps

Extract the user's feature description from their input. Then detect which of these required template sections can be inferred from the description and which are missing:
- **Title** — the feature name/slug
- **user_type** — from "As a [type_of_user]" field
- **goal** — from "I want [goal]" field
- **reason** — from "So that [reason_or_benefit]" field
- **acceptance_criteria** — from the acceptance criteria section (Given/When/Then)
- **definition_of_done** — from the definition of done section

### 4. Ask follow-up questions (up to 3)

For each detected gap, ask a targeted follow-up question in the corresponding template field syntax:

| Missing Field | Follow-up Question Format |
|---|---|
| user_type | "As a [type_of_user] — who is the user for this feature?" |
| goal | "I want [goal] — what should this feature accomplish?" |
| reason | "So that [reason_or_benefit] — why is this feature needed?" |
| acceptance_criteria | "Acceptance criteria — what are the Given/When/Then scenarios for this feature?" |
| definition_of_done | "Definition of done — what criteria must be met for this story to be complete?" |

Prioritize questions by importance if more than 3 gaps are detected:
1. user_type
2. goal
3. reason
4. acceptance_criteria
5. definition_of_done

Limit to a maximum of 3 follow-up questions per session. Collect the user's responses. Ask the user one question at the time.

Handle contradictory information (e.g., user type conflicts with goal context) — flag it and ask for confirmation.

### 5. Fill template

Replace the placeholder sections in the template with the user's input and follow-up answers:

- `<title>` → user's feature title
- `[type_of_user]` → user_type answer
- `[goal]` → goal answer
- `[reason_or_benefit]` → reason answer
- Acceptance criteria section → filled with Given/When/Then scenarios
- Definition of done section → fill with team-level DoD or user input

Perform soft validation: check that all required template sections are filled. If any are blank, warn the user but still proceed to save.

### 6. Generate filename

**6a. Determine sequence number (NN):**
1. Scan the directory `ai/features/todos/` for existing user story files matching the pattern `[NN]_*.md`
2. Extract the highest numeric sequence number present (e.g., if files `01_login.md` and `07_payment.md` exist, highest is `07`)
3. Set `NN = highest + 1`
4. If `NN` is already in use (gap collision), scan for the next available gap in the sequence (e.g., if `01`–`07` are taken and `08` is taken, use `09` or the next gap)

**6b. Generate slug:**
- Convert the feature title to lowercase
- Replace spaces with underscores
- Remove special characters
- Example: "Add User Authentication" → `add_user_authentication`

**6c. Construct filename:**
```
[NN]_[slug].md
```

Check if the generated filename already exists in `ai/features/todos/`. If it does:
- Present three options to the user:
  - (A) Overwrite the existing file
  - (B) Create with the next available sequence number
  - (C) Cancel
- Wait for the user's response before proceeding.

### 7. Ensure output directory exists

If `ai/features/todos/` does not exist, create it automatically.

### 8. Save the file

Write the filled template to `ai/features/todos/[filename]`.

If the write operation fails:
- Catch the error (permission denied, disk full, etc.)
- Display a clear message to the user with the OS-level reason (e.g., "Could not save the user story file. Disk is full (error code: ENOSPC).")
- Abort the flow.

### 9. Confirm completion

Tell the user the file has been saved and provide the full path. Example:
```
Done! The user story has been saved as:
ai/features/todos/[NN]_[slug].md
```

## Edge Cases Summary

| Scenario | Behavior |
|---|---|
| Template file missing | Warn and abort |
| Output directory missing | Create automatically |
| Username gap collision | Find next available gap, use that |
| Generated filename already exists | Prompt for overwrite / next sequence / cancel |
| Write error (permission/disk) | Catch and show OS-level error to user |
| More than 3 gaps | Prioritize by importance, ask only 3 |

## Sequence Number Lifecycle

```
Start → Scan ai/features/todos/ for existing [NN]_*.md files
      → Extract highest numeric prefix (e.g., 07 from 07_login.md)
      → Set NN = highest + 1 (e.g., 08)
      → If NN already exists → scan for next gap
      → Use that NN
      → Save file with NN
```

## Example Flow

```
User: I want to create a new feature for exporting payment reports as CSV
Skill: As a [type_of_user] — who is the user for this feature?
User: Admin
Skill: I want [goal] — what should this feature accomplish?
User: Export payment data filtered by date range
Skill: So that [reason_or_benefit] — why do admins need this?
User: To run financial analysis offline
Skill: [Saves ai/features/todos/08_export_payment_reports_csv.md]
Skill: Done! File saved as 08_export_payment_reports_csv.md
```
