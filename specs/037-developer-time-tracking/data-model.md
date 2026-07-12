# Data Model: Developer Time Tracking

## Entities

### Developer

A contributor identified by git author email.

| Field | Type | Description |
|-------|------|-------------|
| email | string | Git author email (unique identifier) |
| name | string | Git author name (for display only) |

**Uniqueness**: Email is the canonical key. No two developers share the same email within a repository's history.

### Commit Activity Day

Aggregated activity for a single developer on a single date.

| Field | Type | Description |
|-------|------|-------------|
| developer_email | string | Reference to Developer.email |
| date | date (YYYY-MM-DD) | Calendar date in repo-local timezone |
| work_blocks | list[WorkBlock] | Ordered list of continuous work periods |
| total_hours | decimal | Sum of all work block durations |
| files_changed | set[string] | Distinct file paths modified across all commits |

**Derivation**: Built from raw commit data grouped by (author_email, commit_date).

### WorkBlock

A continuous period of commit activity with no gaps >= 1 hour between consecutive commits.

| Field | Type | Description |
|-------|------|-------------|
| start_timestamp | epoch seconds | Timestamp of the first commit in the block |
| end_timestamp | epoch seconds | Timestamp of the last commit in the block |
| duration_hours | decimal | (end - start) / 3600 |

**Boundary rule**: Consecutive commits with < 3600 seconds between them belong to the same block. A gap >= 3600 seconds ends the current block and starts a new one.

### CSV Output Row

The flat representation written to the CSV file.

| Column | Format | Example |
|--------|--------|---------|
| Developer | Author name from git | `Jane Smith` |
| Date | ISO 8601 (YYYY-MM-DD) | `2026-07-11` |
| Hours | Decimal number | `3.5` |
| Files Count | Integer | `12` |

## Relationships

```
Developer (1) ──< (N) CommitActivityDay
CommitActivityDay (1) ──< (N) WorkBlock
CSV Output Row = Denormalized view of CommitActivityDay + Developer.name
```

## Validation Rules

- A CommitActivityDay must have at least 1 WorkBlock (otherwise no data exists for that day).
- A WorkBlock must have duration >= 0 hours (single commit = 0 duration).
- File paths are case-sensitive per the filesystem.
- CSV rows are sorted by date ascending, then developer email ascending.
