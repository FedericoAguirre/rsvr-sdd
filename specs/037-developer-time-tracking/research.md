# Research: Developer Time Tracking (CSV Export)

## Decisions

### Developer Identification

- **Decision**: Use git author email as the unique developer identifier (not name).
- **Rationale**: Author email is globally unique within a repository; names can collide. This matches standard git identity practices (commit attribution by email).
- **Alternatives considered**: Author name only (too ambiguous), name+email combined (unnecessary complexity for CSV readability).

### Hours Calculation Algorithm

- **Decision**: Sum of active work blocks per developer per date. A work block is a sequence of consecutive commits with no gap >= 1 hour between them.
- **Rationale**: Accurately reflects actual working time by excluding long pauses (lunch, meetings). Matches user requirement.
- **Implementation approach**: Sort commits by timestamp per developer-date, iterate to identify gaps >= 3600 seconds, sum block durations.

### Output Format

- **Decision**: CSV with optional `-o <path>` flag (defaults to `developer-time.csv`). Dates in ISO 8601 (YYYY-MM-DD), hours as decimal numbers.
- **Rationale**: CSV is universally consumable by spreadsheets and analysis tools. ISO 8601 is unambiguous and sortable. Decimal hours enable easy summation/charting.
- **Alternatives considered**: hh:mm format (harder to compute), stdout-only (less convenient for repeated runs).

### Error Handling

- **Decision**: Errors to stderr, non-zero exit code on failure, exit 0 on success.
- **Rationale**: Standard CLI convention. Stderr separates diagnostic output from data output, preventing CSV corruption when redirecting.

### Testing Approach

- **Decision**: Manual verification against a controlled test repository with known commit timestamps. Snapshot-based (expected CSV compared against actual output).
- **Rationale**: TDD is not practical for a pure data-transform shell script. The script's output is deterministic given its input (git history), making snapshot comparison sufficient.
- **Alternatives considered**: bats test framework (adds dev dependency, disproportionate for a single-file script).

### i18n Decision

- **Decision**: No i18n for this tool. Error messages and help text are written in English only.
- **Rationale**: The zero-dependency constraint prevents using gettext or similar i18n mechanisms in a standalone shell script. The script has fewer than 10 human-readable strings. Tool is internal to the team.

### Platform Compatibility

- **Decision**: Target POSIX-compatible systems (Linux, macOS). Use `awk` for timestamp math (available on both platforms).
- **Rationale**: Project constraint requires POSIX compatibility. `awk` is the most portable tool for epoch-second calculations across platforms.
- **macOS caveat**: BSD `date` differs from GNU `date` — rely on `awk` for date arithmetic instead of `date -d`.
