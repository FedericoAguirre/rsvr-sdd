# Data Model: User Story Helper Skill

## Entities

### Skill Definition
Represents the opencode skill configuration file.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | string (kebab-case) | Skill identifier: `user-story-helper` |
| `description` | string | Capability summary + trigger phrases for activation |
| file path | string | `.agents/skills/user-story-helper/SKILL.md` |

### Template
The source markdown file that defines the user story structure.

| Attribute | Type | Description |
|-----------|------|-------------|
| file path | string | `ai/templates/user_story_template.md` (exists) |
| sections | list | Title, User story (As a / I want / So that), Acceptance criteria (Given/When/Then), Definition of Done |

### User Story (Output File)
A saved markdown file in `ai/features/todo/`.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| filename | string | `[NN]_[slug].md` — 2-digit sequence, underscore-separated lowercase slug |
| sequence | integer (01–99) | Auto-incremented from highest existing; gap-filling if collision detected |
| title | string | User story title (from template `<title>` placeholder) |
| user_type | string | `As a [type_of_user]` — who the feature is for |
| goal | string | `I want [goal]` — what the feature should do |
| reason | string | `So that [reason_or_benefit]` — why the feature is needed |
| acceptance_criteria | list of Gherkin scenarios | `Given [context], When [action], Then [outcome]` |
| definition_of_done | string | Team-level DoD criteria |

### Sequence Number Lifecycle
```
Start → Scan ai/features/todo/ for existing files
      → Extract highest numeric prefix (e.g., 07 from 07_login.md)
      → Set NN = highest + 1 (e.g., 08)
      → If 08 already exists → scan for next gap → use that
      → Save file with NN
```

## Relationships

```
Skill Definition (1) ──reads──→ Template (1)
Skill Definition (1) ──creates──→ User Story (many)
```
