# Research: CSV Client Upload

## CSV Parsing Approach

**Decision**: Use Python stdlib `csv.DictReader` for CSV parsing.

**Rationale**: `csv.DictReader` maps CSV columns to dictionary keys via the header row, making field access readable and column-order-independent. Built-in, no third-party dependency needed.

**Alternatives considered**:
- `csv.reader` — positional indexing is fragile if column order changes
- `pandas` — heavy dependency, overkill for this use case
- Manual string splitting — error-prone, no quote/escape handling

## Matching Logic

**Decision**: Multi-pass matching with priority: name → email → mobile.

**Rationale**: Name matching is most reliable for identifying existing clients. Email and mobile serve as fallback for reconnecting records where names have changed. Each row matches at most one existing client.

**Implementation details**:
1. Case-insensitive match on `first_name` + `last_name` (after trimming)
2. If no name match, case-insensitive match on `email`
3. If no email match, match on `mobile`
4. If no match at all, create new client with `is_active=True`

## Data Cleansing

**Decision**: Trim whitespace from all fields, normalize empty strings to `None` for optional fields.

**Rationale**: Prevents matching failures due to leading/trailing spaces and avoids storing empty strings instead of NULL in the database.

## Error Handling

**Decision**: Row-level error handling — invalid rows are skipped and counted as errors; valid rows in the same file are still processed.

**Rationale**: A single malformed row should not block the entire batch. The summary report shows exactly how many rows succeeded and failed.

## UI Pattern

**Decision**: Django form with `FileField` + HTMX for the upload page. Results shown as a summary on the same page after processing.

**Rationale**: Consistent with existing Django form patterns in the project. HTMX not strictly required here (form submission via POST with page reload is acceptable), but can use HTMX for better UX if desired.
