# Research: Rename Exported Reservations PDF

## Overview

All technical context was already known from codebase exploration. No NEEDS
CLARIFICATION items existed for this feature — language, framework,
dependencies, and architecture were confirmed by reading existing source.

## Decisions

### Filename format

- **Decision**: `reservations_<class>_YYYYMMDD.pdf`
- **Rationale**: Matches user requirement verbatim. Uses underscores as
  separators (consistent with common file naming conventions). Date uses
  compact YYYYMMDD (machine-sortable, no separators).
- **Alternatives considered**: `reservations-<class>-YYYY-MM-DD.pdf`
  (rejected — user explicitly requested underscores and compact date)

### Class slot name sanitization

- **Decision**: Replace spaces with underscores; remove characters invalid
  in cross-platform filenames (`/`, `\0`, `<`, `>`, `:`, `"`, `|`, `?`, `*`)
- **Rationale**: Ensures the file can be downloaded and saved on any OS
  without errors.
- **Alternatives considered**: Percent-encoding (rejected — overkill for
  filenames); stripping non-alphanumeric entirely (rejected — class name
  readability lost); keeping as-is (rejected — invalid on Windows)

### Date format transformation

- **Decision**: Convert `YYYY-MM-DD` (from query param) to `YYYYMMDD` by
  removing dashes.
- **Rationale**: Minimal transformation, matches user requirement.
- **Alternatives considered**: `datetime.strftime("%Y%m%d")` parsing
  (more robust, but dashes-removal is sufficient since format is validated)

### Implementation location

- **Decision**: Single line change in `reservation_list_pdf` view's
  `Content-Disposition` header (line 59 of `views.py`).
- **Rationale**: The filename is constructed inline; no helper to extract.
  Adding a dedicated helper function would violate YAGNI for a one-liner.
- **Alternatives considered**: Extracting to a utility function (rejected
  — YAGNI violation for a single call site)
