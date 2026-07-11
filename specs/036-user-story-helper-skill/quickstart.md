# Quickstart: User Story Helper Skill

## Prerequisites

- opencode installed and configured
- The `user-story-helper` skill must be in the loaded skills list (should auto-detect from `.agents/skills/user-story-helper/SKILL.md`)

## Usage

1. **Trigger the skill** by saying one of these phrases:
   - "I want to create a new feature for [description]"
   - "I want to create a user story for [description]"
   - "New feature idea: [description]"

2. **Answer follow-up questions** (if any):
   The skill will ask up to 3 questions if your initial description is missing:
   - Who is the user type? (As a...)
   - What is the goal? (I want...)
   - What is the benefit? (So that...)
   - Are there acceptance criteria?

3. **Review the saved file**:
   The skill will save the completed user story to:
   ```
   ai/features/todo/[NN]_[slug].md
   ```
   The filename uses the next available 2-digit sequence number.

4. **If the file already exists**, you will be prompted to:
   - A) Overwrite the existing file
   - B) Create with the next available sequence number
   - C) Cancel

## Example

```
You: I want to create a new feature for exporting payment reports as CSV
Skill: As a [type_of_user] — who is the user for this feature?
You: Admin
Skill: I want [goal] — what should this feature accomplish?
You: Export payment data filtered by date range
Skill: So that [reason_or_benefit] — why do admins need this?
You: To run financial analysis offline
Skill: [Saves ai/features/todo/08_export_payment_reports_csv.md]
Skill: Done! File saved as 08_export_payment_reports_csv.md
```

## Verification

After saving, check the file at `ai/features/todo/[NN]_[slug].md` contains all template sections filled.
