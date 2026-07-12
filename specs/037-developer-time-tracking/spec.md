# Feature Specification: Developer Time Tracking (CSV Export)

**Feature Branch**: `037-developer-time-tracking`

**Created**: 2026-07-11

**Status**: Draft

**Input**: User description: "Track developer invested time in the project via a CSV file with developer, date, hours, and created/updated files count, using only standard shell commands."

## Clarifications

### Session 2026-07-11

- Q: How should the script uniquely identify developers when grouping commits? → A: Author email.
- Q: Where should the CSV output be written? → A: Accept optional `-o` argument, default to `developer-time.csv`.
- Q: How should errors be reported? → A: Errors to stderr, non-zero exit code on failure.
- Q: Hours precision format in CSV? → A: Decimal hours (e.g., `2.5`).
- Q: Date format in CSV? → A: ISO 8601 (YYYY-MM-DD).

### Session 2026-07-11 (Implementation)

- Q: CSV quoting strategy for special characters? → A: Quote all fields with double quotes.
- Q: Output file overwrite behavior for existing files? → A: Overwrite silently (standard Unix CLI convention).
- Q: Gap threshold — >= 1hr or > 1hr? → A: >= 1hr (>= 3600s).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run CLI Tool to Generate CSV (Priority: P1)

As a project manager, I want to run a single CLI command (no arguments) that analyzes the entire git history and produces a CSV file with each developer's daily activity, so that I can assess team productivity without installing any external tools.

**Why this priority**: This is the core value proposition — generating the CSV with correct data. Without this, the feature has no value.

**Independent Test**: Can be tested independently by running the script in any git repository and verifying CSV output contains the expected headers and rows.

**Acceptance Scenarios**:

1. **Given** a git repository with commit history, **When** the script is executed with no arguments, **Then** a CSV file is created with headers: Developer, Date, Hours, Files Count.

2. **Given** a developer made commits on multiple dates, **When** the CSV is inspected, **Then** each developer-date pair appears as a separate row with its own hours and file count.

3. **Given** a developer made no commits on a given date, **When** the CSV is inspected, **Then** no row exists for that developer on that date.

---

### User Story 2 - Accurate Hours Calculation (Priority: P1)

As a project manager, I want hours worked per developer per date to reflect actual activity blocks, so that the time investment metric is fair and useful for analysis.

**Why this priority**: Hours calculation is the most technically complex part and directly impacts the trustworthiness of the data.

**Independent Test**: Can be tested independently by creating a known commit pattern (timestamps) and verifying the output hours match the expected duration accounting for gaps.

**Acceptance Scenarios**:

1. **Given** a developer has commits at 9:00, 9:30, and 10:00 on the same date, **When** the script runs, **Then** hours for that developer-date equals 1.0 (from 9:00 to 10:00, no gap >1hr).

2. **Given** a developer has commits at 9:00 and 11:30 on the same date, **When** the script runs, **Then** hours equals 2.5 (from 9:00 to 11:30, no gap >1hr).

3. **Given** a developer has commits at 9:00-10:00 and 14:00-15:00 with a 4-hour gap in between, **When** the script runs, **Then** hours equals 2.0 (each block counted separately, the gap is excluded).

4. **Given** a developer's commits span past midnight into the next day, **When** the script runs, **Then** the hours are attributed to the date of the first commit in each session.

---

### User Story 3 - File Change Count (Priority: P2)

As a project manager, I want the CSV to include a count of files created or modified by each developer per date, so that I can correlate time investment with output volume.

**Why this priority**: File count is a valuable secondary metric but the core value is hours. This can be added after hours logic is working.

**Independent Test**: Can be tested independently by checking distinct file paths per developer-date in the CSV against known git history.

**Acceptance Scenarios**:

1. **Given** a developer modified 3 distinct files in their commits on a date, **When** the CSV is inspected, **Then** Files Count equals 3 for that row.

2. **Given** a developer modified the same file multiple times on a date, **When** the CSV is inspected, **Then** Files Count counts that file only once.

---

### User Story 4 - Help and Documentation (Priority: P3)

As a project manager, I want the tool to have a `--help` flag and basic documentation, so that I and other team members can understand how to use it.

**Why this priority**: Important for usability but not required for the core functionality to work.

**Independent Test**: Can be tested by invoking the script with `--help` flag and verifying output describes usage.

**Acceptance Scenarios**:

1. **Given** the script is run with `--help` or without a recognized flag, **When** the command executes, **Then** usage instructions are printed to stdout.

---

### Edge Cases

- **Empty repository**: What happens when the repository has no commits? The script should output a CSV with only headers or a message indicating no activity found.
- **New developer with one commit**: A single commit on a date should result in 0 hours for that developer-date (or a minimal duration).
- **Multiple timezones**: How are commits from different timezones handled? Git stores timestamps in UTC or a consistent format — the script should handle standard git date formats.
- **Binary files**: Renames or binary files count as modified files but should not cause errors.
- **Large repositories**: Repository with 10,000+ commits across many developers — the script should complete in reasonable time.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: CLI script MUST analyze the current git repository with no required arguments; running with no arguments uses defaults.
- **FR-002**: Script MUST analyze the entire git commit history (all branches).
- **FR-003**: Output MUST be a CSV file with columns: Developer, Date, Hours, Files Count. All fields MUST be quoted with double quotes (e.g., `"Jane Smith","2026-07-11","2.5","12"`). Dates MUST be in ISO 8601 format (YYYY-MM-DD). Hours MUST be expressed as decimal numbers (e.g., `2.5` for 2 hours 30 minutes).
- **FR-004**: Hours MUST be calculated as the sum of active work blocks per developer per date, where a work block is defined as consecutive commits with no gap of one hour or more between them.
- **FR-005**: Each gap of 3600 seconds (1 hour) or more between consecutive commits on the same date MUST start a new work block for that developer-date.
- **FR-006**: Files Count MUST count distinct files (created or modified) per developer per date, regardless of how many times each file was changed.
- **FR-007**: Script MUST run using only standard shell commands available on a typical Unix system (sh/awk/sed/git, etc.).
- **FR-008**: Script MUST accept a `--help` flag that prints usage documentation.
- **FR-009**: Script MUST handle repositories with no commits gracefully (output headers only or a clear message).
- **FR-010**: Script SHOULD complete analysis of a repository with 10,000 commits in under 30 seconds on modern hardware.
- **FR-011**: Script MUST accept an optional `-o <path>` argument to specify the CSV output path; if omitted, the file MUST be written to `developer-time.csv` in the current directory.
- **FR-012**: Script MUST print error messages to stderr and exit with a non-zero exit code on failure; on success it MUST exit with code 0.

### Key Entities *(include if feature involves data)*

- **Developer**: A contributor uniquely identified by git author email. Attributes: name, email.
- **Commit Activity Day**: A developer's work on a single date. Attributes: developer, date, list of work blocks, total hours, files modified.
- **Work Block**: A continuous period of commit activity with no gaps of one hour or more. Attributes: start timestamp, end timestamp, duration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A project manager can generate the CSV by running a single command with no arguments, without installing any software.
- **SC-002**: The CSV is generated in under 30 seconds for a repository with up to 10,000 commits across 10+ developers.
- **SC-003**: For a controlled test repository with known commit timestamps, the calculated hours match the expected values to within 1 minute precision.
- **SC-004**: File counts match the number of distinct files modified per developer per date when verified against `git log` output.
- **SC-005**: The script produces consistent results across different Unix environments (macOS, Linux) without requiring any package installation.

## Assumptions

- The repository is a standard git repository with git available on the system PATH.
- Developers are uniquely identified by their git author email. Author name is included in the CSV for readability but is not used for grouping.
- All commit timestamps are in the same timezone or are stored in git's standard format (Unix timestamp or ISO 8601).
- The script is intended for Unix-like systems (macOS/Linux). Windows support via WSL or Git Bash is considered acceptable but not a primary target.
- The project manager running the script has access to the repository filesystem and can execute shell scripts.
- No external dependencies beyond git and standard POSIX utilities (sh, awk, sort, uniq, etc.) are required.
- The feature does not include a scheduled/cron-based execution or any persistent storage — it runs on-demand only.
