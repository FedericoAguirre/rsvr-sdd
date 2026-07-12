# CLI Contract: developer-time.sh

## Synopsis

```text
scripts/developer-time.sh [-o <output_path>] [--help]
```

## Description

Analyzes the git repository at the current working directory and generates a CSV report of developer activity time.

## Arguments

| Argument | Description |
|----------|-------------|
| `-o <path>` | Output file path (default: `developer-time.csv` in current directory) |
| `--help` | Print usage information and exit |

No positional arguments. The script analyzes the repository at `$(pwd)`.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — CSV written successfully |
| 1 | Error — repository issue (no git repo, no commits) |
| 2 | Error — invalid arguments |

## Output Format

### Success

A UTF-8 CSV file with the following columns (no BOM), all fields quoted with double quotes:

```csv
"Developer","Date","Hours","Files Count"
"Jane Smith","2026-07-11","3.50","12"
```

- **Developer**: Author name from git commit metadata
- **Date**: ISO 8601 date (YYYY-MM-DD) in the timezone of the commit timestamps
- **Hours**: Decimal hours, summed across all work blocks for that developer-date
- **Files Count**: Count of distinct file paths modified across all commits for that developer-date

Rows are sorted by date ascending, then developer name alphabetically.

### Error

Error messages are printed to stderr. No CSV output is written on error.

```text
Error: Not a git repository: /path/to/dir
Error: No commits found in repository
Error: Unknown option: --invalid-flag
```

## Environment

The script requires:
- `git` available on PATH
- Standard POSIX utilities: `awk`, `sort`, `uniq`, `cut`
- No other dependencies

## Examples

```sh
# Generate CSV with default output path
scripts/developer-time.sh

# Specify a custom output path
scripts/developer-time.sh -o /tmp/team-activity.csv

# Display help
scripts/developer-time.sh --help
```
