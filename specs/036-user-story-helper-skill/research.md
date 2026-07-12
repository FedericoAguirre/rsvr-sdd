# Research: User Story Helper Skill

## SKILL.md Format Convention

All existing skills in `.agents/skills/*/SKILL.md` follow this structure:

```yaml
---
name: <kebab-case-name>
description: <descriptive text that also serves as trigger phrase definition>
---
```

Key observations:
- `name` is always kebab-case (e.g., `django-expert`, `frontend-design`)
- `description` is a single paragraph that starts with a capability summary and lists trigger phrases at the end
- Some skills have `license` and `metadata.author/version` fields (optional)
- The body after frontmatter is markdown instructions for the AI agent
- No external dependencies, no code — pure configuration/instructions

## Trigger Phrase Design

The trigger phrases should be embedded in the `description` field. Based on the spec:
- "I want to create a new feature"
- "I want to create a user story"
- "new feature idea"

These phrases should be listed at the end of the description field, similar to how existing skills structure it.

## Filename Convention

From `ai/features/todos/` and `ai/features/done/` — existing files use patterns like:
- `01-deployment-script-windows.md`
- `03_sending_clients_classes_calendar.md`
- `06-1-stacked-graph-weekly-grouping.md`

The spec specifies `[NN]_[slug].md` with underscore separator and lowercase slug.

## Decisions

- **Format**: Follow minimal frontmatter (name + description) used by django-expert and frontend-design skills — no license/metadata unless needed
- **Trigger phrases**: Embed in description field as comma-separated list
- **Instructions**: Direct the AI to load the template, detect gaps, ask follow-ups (max 3), validate with soft checks, and save with sequential filename
