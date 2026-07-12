# Quickstart: Developer Time Tracking

## Prerequisites

- git
- Standard POSIX utilities (awk, sort, uniq, cut)
- A git repository with commit history

## Usage

```sh
# Navigate to the repository to analyze
cd /path/to/repo

# Generate the CSV
scripts/developer-time.sh

# The file developer-time.csv is created in the current directory
```

## Custom Output Path

```sh
scripts/developer-time.sh -o reports/team-hours.csv
```

## View Help

```sh
scripts/developer-time.sh --help
```

## CSV Output Example

```csv
Developer,Date,Hours,Files Count
Jane Smith,2026-07-11,3.5,12
John Doe,2026-07-11,5.0,8
Jane Smith,2026-07-12,2.0,4
```

## Next Steps

- Open the CSV in any spreadsheet software for charting and analysis
- Use `sort -t, -k2` to reorder by date if needed
- Pipe through `awk -F, '{sum+=$3} END {print sum}'` for total hours across all developers
