# Data Model: AI Development Data Collection

## Overview

This feature reads from three existing data sources (no new database tables) and produces one output artifact. No Django models are created or modified.

## Data Sources

### Source 1: `ai/features/done/*.md`

Feature completion records. Each file is a Markdown document whose first `# ` heading is the feature title.

**Relevant fields**:
- `title` — first `# ` line content (e.g., `# Track Developer Invested Time (CSV Export)`)
- `filename` — base filename for cross-referencing (e.g., `01_track_developer_invested_time.md`)

### Source 2: `specs/???-*/spec.md`

Feature specification documents. Each spec file follows the standard template with sections for acceptance criteria, constraints, examples, edge cases, assumptions, key entities, and success criteria.

**Relevant fields**:
- `section_presence` — which sections exist in the spec (determines `specs_quality` score)

### Source 3: `ai/sessions/*.md`

AI session logs. Each file records an AI-assisted development session.

**Relevant fields**:
- `model` — `**Model:**` or `**Model**:` metadata field
- `date` — `**Date:**` metadata field
- `session_timestamp` — from filename timestamp (e.g., `20260717T220000Z`)
- `commands` — `/speckit.specify` and `/speckit.implement` references in session body
- `feature_ref` — derived from filename prefix or slug

## Output Schema

### CSV Row

| Column | Type | Description | Source |
|--------|------|-------------|--------|
| `feature` | string | Feature title (`#` heading from done/ file) | `ai/features/done/*.md` |
| `complexity` | integer (1, 2, 3, 5, 8) | Estimated complexity based on session count, iterations, reviews, bug fixes | Derived from sessions + heuristics |
| `minutes` | integer | Elapsed minutes from first `/speckit.specify` to PR/merge | Derived from session timestamps |
| `model` | string | AI model name used for implementation | `ai/sessions/*.md` — `**Model:**` field |
| `start_timestamp` | ISO 8601 | Timestamp of first `/speckit.specify` command | First session file date/timestamp |
| `end_timestamp` | ISO 8601 | Timestamp of PR/merge command | Last session file date/timestamp or git log |
| `specs_quality` | integer (1–5) | Quality score based on spec section completeness | `specs/*/spec.md` — section presence analysis |
| `iterations` | integer | Count of `/speckit.specify` and post-implement AI calls | Session logs — command mentions |

## Cross-Reference Strategy

```
Given: ai/features/done/{slug}.md
  → Extract feature number (e.g., "01_track_developer_invested_time" → "01")
  → Match specs/{num}-{slug}/spec.md by number prefix
  → Match ai/sessions/ files by number or slug in filename
```

### Resolution algorithm

1. List all files in `ai/features/done/`
2. For each file, extract the filename and title
3. Determine candidate spec directories by scanning `specs/{num}-*/spec.md`
4. Match to sessions by scanning `ai/sessions/` for files containing the feature number or slug
5. Collect all matched sessions and extract metadata
6. Compute complexity, minutes, iterations from collected data

## Validation Rules

| Field | Rule |
|-------|------|
| `feature` | Must not be empty |
| `complexity` | Must be one of: 1, 2, 3, 5, 8 |
| `minutes` | Must be a non-negative integer |
| `model` | May be empty if session file lacks model field |
| `start_timestamp` | ISO 8601 format; may be empty if missing |
| `end_timestamp` | ISO 8601 format; must be ≥ start_timestamp when both present |
| `specs_quality` | Must be integer 1–5; defaults to 1 if no spec file found |
| `iterations` | Must be non-negative integer; defaults to 1 |
