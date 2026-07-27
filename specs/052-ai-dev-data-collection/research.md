# Research: AI Development Data Collection

## Research Tasks

### R1: Correlation between ai/features/done/ and ai/sessions/

**Decision**: Correlate features to sessions by matching the feature number prefix (e.g., `15-list-unassociated-user-reservations` → session files containing `048`, `049`, `050` etc.) and by feature slug in session filenames. Where session filenames include a feature number (e.g., `deepseek-v4-flash-free-048-session-summary-20260717T220000Z.md`), the prefix `048` maps to the feature's spec directory under `specs/048-*`. Feature files in `done/` have matching slugs.

**Rationale**: Examination of existing data shows two naming conventions:
1. Modern sessions: `{model}-{feature_num}-{slug}-{timestamp}.md` — directly maps to `specs/{feature_num}-{slug}/`
2. Legacy sessions: `{model}_{slug}_{date}.md` — maps by slug and date

**Alternatives considered**:
- Relying solely on git log to match commits to features — more accurate but requires git history access
- Cross-referencing spec directory names vs session filenames — current approach; most reliable

### R2: Timestamp extraction from session files

**Decision**: Extract `start_timestamp` from the first session file's date/timestamp (earliest session matching the feature) and `end_timestamp` from the last session file or the PR/merge timestamp.

**Rationale**: Session files contain either:
- A `**Date:**` metadata field with YYYY-MM-DD format
- A timestamp in the filename (e.g., `20260717T220000Z`)
- A session heading with date context

**Alternatives considered**:
- Using git commit timestamps — more precise but requires git access and parsing
- Using file modification times — unreliable after git clones

### R3: Complexity calculation approach

**Decision**: Derive complexity from:
- Number of session files for the feature (proxy for iterations)
- Number of `/speckit.*` commands recorded in session logs
- Whether bug fixes are mentioned in session summaries
- Whether multiple review cycles are indicated

**Rationale**: The spec defines complexity as 1, 2, 3, 5, or 8 based on iterations, clarifications, tasks, and reviews. Session logs contain "Commits" sections and "Summary" sections that indicate the scope of work. Cross-referencing session count with described work gives a reliable complexity estimate.

**Alternatives considered**:
- Hardcoded values in a lookup table — requires manual maintenance
- LLM-based classification — overengineered for this context

### R4: Specs quality assessment

**Decision**: Parse the spec file (`specs/{num}-{slug}/spec.md`) and check for the presence of sections:
- **Level 1**: Any content exists (description)
- **Level 2**: Has "Acceptance Criteria" or "Acceptance Scenarios" section
- **Level 3**: Has "Constraints" or "Constraints" notes in Technical Context
- **Level 4**: Has concrete examples in acceptance scenarios
- **Level 5**: Has additional elements (Edge Cases, Assumptions, Key Entities, Success Criteria)

**Rationale**: The spec quality definitions map directly to spec.md section presence. Each spec already follows the standard template which includes these sections.

**Alternatives considered**:
- Manual quality rating — not scalable
- Section word count heuristic — less reliable than presence/absence

### R5: Iterations count

**Decision**: Count of `/speckit.specify` commands in session logs plus `/speckit.implement` invocation count (per spec definition: "The number of /speckit.specify commands calls or ai calls after /speckit.implement command").

**Rationale**: Session logs contain "Commits" sections that list all commands. Parsing for `/speckit.specify` and post-`/speckit.implement` AI calls provides the iteration count.

**Alternatives considered**:
- Counting session files — simpler but less accurate
- Counting git commits — broader scope than AI-specific iterations

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CSV generation | Python stdlib `csv` module | No new dependencies needed |
| File parsing | Python stdlib `pathlib` + `re` for patterns | Available in Python 3.12 stdlib |
| Management command | Django `BaseCommand` | Standard Django pattern |
| Date/time parsing | Python stdlib `datetime` + `zoneinfo` | Available in Python 3.12 stdlib |
