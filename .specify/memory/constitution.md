<!--
  Sync Impact Report
  Version change: 2.0.2 → 2.1.0
  Modified principles:
    - III. User Experience Consistency — expanded i18n rule with explicit
      element types, 3-step implementation contract, and AI agent directive
  Added sections: None
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ (no change needed — generic)
    - .specify/templates/spec-template.md ✅ (no change needed — generic)
    - .specify/templates/tasks-template.md ✅ (no change needed — generic)
  Follow-up TODOs: None
-->

# rsvr-sdd Constitution

## Core Principles

### I. Code Quality

All code MUST pass automated linting and static analysis before merge.
No dead code, commented-out code, or unresolved TODOs may be committed.
Code review is REQUIRED for every change. Simplicity is paramount —
apply YAGNI rigorously; every complexity addition MUST be justified in
the Complexity Tracking section of the implementation plan. Formatting
MUST be consistent across the entire codebase (enforced by formatter).

### II. Testing Standards (NON-NEGOTIABLE)

TDD is mandatory. Tests MUST be written and reviewed by the user FIRST,
and MUST fail before implementation begins. The Red-Green-Refactor cycle
MUST be strictly enforced. Integration tests are REQUIRED for new
library contracts, contract changes, inter-module communication, and
shared schema changes. Unit tests alone are INSUFFICIENT for boundary-
crossing changes. Test coverage MUST be measured and reviewed; untested
paths block merge.

### III. User Experience Consistency

All user-facing interfaces MUST follow consistent conventions for:
output formatting, error messages, exit codes, and help text. Error
messages MUST be actionable (state what went wrong AND how to fix it).
CLI output MUST support both human-readable and JSON formats. Every
feature MUST include user-facing documentation updated in the same PR.

**i18n — NON-NEGOTIABLE (Zero Exceptions)**

Every string visible to the user MUST be internationalized via i18n
before the task is considered complete. This rule applies without
exception to ALL of the following element types:

- Headers (&lt;h1&gt;–&lt;h6&gt;, section titles, panel titles)
- Labels (form labels, field names, tooltip text)
- Body text and paragraphs
- Buttons and CTAs
- Links and anchor text
- Tags, badges, and status chips
- Error messages, warnings, and success notifications
- Placeholder text and helper text
- Empty states and fallback messages

**Implementation contract — ALL three steps are REQUIRED:**

1. **Never hardcode strings.** No user-visible text may appear as a
   raw string literal in JSX, templates, or component logic.
2. **Register the key.** Every new string MUST have an entry in the
   i18n translation file before the component is written.
3. **Verify Spanish output.** The rendered UI MUST display the Spanish
   translation. Untranslated strings block merge.

**AI agent (opencode) directive:** Before marking any task done,
scan every component touched in this session for raw user-visible
strings. If any are found, translating them is part of the current
task — not a follow-up.

### IV. Performance Requirements

Every feature MUST define measurable performance criteria before
implementation. All services and libraries MUST use structured logging
for observability. Response latencies and resource usage MUST be
documented as constraints in the implementation plan. Performance
regressions MUST be caught before merge via automated benchmarks or
profiling gates. Profiling data MUST accompany any performance-
sensitive change.

## Technology Constraints

This project uses opencode as its AI integration. Runtime targets are
POSIX-compatible (Linux/macOS). All dependencies MUST be declared
explicitly. No proprietary or closed-source build tools are permitted.

## Development Workflow

All work follows the Specify → Plan → Tasks → Implement cycle with
review gates at each stage. Feature branches MUST use sequential
numbering (`###-feature-name`). Commits MUST be atomic and descriptive.
Each user story MUST be independently testable and deliverable as an MVP
increment. Code quality, UX, and performance checks MUST pass before
merge.

Before creating a PR, an AI session markdown file must be saved in the ai/sessions folder.
The session must be compressed before saving.
The name of the session file must be compound of the LLM model, feature, and timestamp.

If the feature was defined from a ai/features/todos file, move that file into the ai/features/done folder.
Adding the next requests, to the LLM Agent that were not included in the first file version.

## Governance

This constitution supersedes all other practices and is the single source
of truth for project governance. Amendments require:
1. Documented rationale describing the need for change
2. Stakeholder approval before implementation
3. A migration plan for any transitional impacts
4. A constitution version bump following semantic versioning

All PRs and reviews MUST verify constitutional compliance. Complexity
additions MUST be justified in the Complexity Tracking section of the
plan. Non-negotiable principles (Testing Standards) cannot be amended —
only clarified. All project artifacts follow MAJOR.MINOR.PATCH semantic
versioning. Breaking changes MUST increment MAJOR; new backward-
compatible functionality increments MINOR; bug fixes increment PATCH.

**Version**: 2.1.0 | **Ratified**: 2026-06-07 | **Last Amended**: 2026-06-24
