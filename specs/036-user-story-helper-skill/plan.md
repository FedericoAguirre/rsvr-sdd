# Implementation Plan: User Story Helper Skill

**Branch**: `036-user-story-helper-skill` | **Date**: 2026-07-10 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/036-user-story-helper-skill/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Create the `user-story-helper` opencode skill at `.agents/skills/user-story-helper/SKILL.md` that loads `ai/templates/user_story_template.md`, asks up to 3 clarifying questions when the user's description is incomplete, validates output with soft checks, and saves the filled template to `ai/features/todo/[NN]_[slug].md` with a unique sequential filename.

## Technical Context

**Language/Version**: Markdown + YAML frontmatter (SKILL.md format per opencode conventions)

**Primary Dependencies**: None — pure opencode skill configuration, no runtime dependencies

**Storage**: File system — reads from `ai/templates/user_story_template.md`, writes to `ai/features/todo/`

**Testing**: Manual acceptance verification via opencode conversation (trigger phrases, output file inspection)

**Target Platform**: opencode AI integration (all compatible models — confirmed model-agnostic)

**Project Type**: opencode skill (SKILL.md with YAML frontmatter following `.agents/skills/*/SKILL.md` conventions)

**Performance Goals**: N/A — conversational interaction

**Constraints**: Must follow existing SKILL.md format (YAML frontmatter with name, description, license, metadata). No new runtime dependencies. Skill must be model-agnostic.

**Scale/Scope**: Single skill definition file at `.agents/skills/user-story-helper/SKILL.md`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Justification |
|------|--------|---------------|
| **I. Code Quality** | ✅ PASS | No code to lint — skill is a configuration/instruction file (SKILL.md). YAGNI applies (single skill, no complexity). |
| **II. Testing Standards** | ✅ PASS | TDD applies to application code. This is an AI agent configuration file — no programmatic runtime exists to test. Acceptance is verified via opencode conversation. |
| **III. UX Consistency / i18n** | ✅ PASS | i18n applies to user-facing application strings. The SKILL.md is tool configuration, not application UI. Trigger phrases and skill description are in English by design (opencode conventions). |
| **IV. Performance** | ✅ PASS | No runtime performance considerations for a configuration file. |

All gates pass. No Complexity Tracking needed.

### Post-Design Re-evaluation

| Gate | Status | Notes |
|------|--------|-------|
| **I. Code Quality** | ✅ PASS | Single SKILL.md file — YAGNI satisfied. No code to format/lint. |
| **II. Testing Standards** | ✅ PASS | No application code; acceptance verified via opencode conversation. |
| **III. UX Consistency / i18n** | ✅ PASS | Skill description and AI instructions are opencode configuration, not application UI strings. Other skills follow same pattern. |
| **IV. Performance** | ✅ PASS | No runtime component. |

**Result**: All gates pass post-design. Proceeding.

## Project Structure

### Documentation (this feature)

```text
specs/036-user-story-helper-skill/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (empty — no external interfaces)
├── spec.md              # Feature specification
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
.agents/skills/user-story-helper/
└── SKILL.md             # Skill definition (the deliverable)

ai/
├── templates/
│   └── user_story_template.md  # Input template (exists)
└── features/
    └── todo/            # Output directory (exists)
```

**Structure Decision**: Single skill file at `.agents/skills/user-story-helper/SKILL.md` following the same convention as the 7 existing skills in `.agents/skills/`. No application source code changes needed.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. Section left empty.
