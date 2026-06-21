# CSV File Format Contract

## Source of Truth

This document defines the expected format, columns, and constraints for CSV files uploaded via the client import feature.

## File Format

| Property | Value |
|----------|-------|
| **Encoding** | UTF-8 (BOM optional) |
| **Delimiter** | Comma (`,`) |
| **Quote character** | Double-quote (`"`) |
| **Header row** | Required (first row) |
| **Line endings** | CRLF or LF |
| **Max file size** | 5 MB |

## Columns

| Column | Required | Type | Max Length | Notes |
|--------|----------|------|------------|-------|
| `first_name` | Yes | string | 100 | Trimmed. Must be non-empty after trimming. |
| `last_name` | Yes | string | 100 | Trimmed. Must be non-empty after trimming. |
| `email` | No | email | 254 | Trimmed. Empty → null. `unique` in DB. |
| `mobile` | No | string | 20 | Trimmed. Empty → null. `unique` in DB. |

**At least one of `email` or `mobile` must be provided** (per row).

## Column Name Handling

- Column names in the CSV header are case-insensitive.
- Leading/trailing whitespace in column names is trimmed.
- Unknown columns are ignored.
- If a required column is missing, the file is rejected with an error message listing the missing columns.

## Matching Priority

For each row, attempt to match to an existing `Client` in the following order:

1. **Name match**: `first_name` + `last_name` (case-insensitive, trimmed)
2. **Email match**: `email` (case-insensitive, trimmed, only if email is non-null)
3. **Mobile match**: `mobile` (trimmed, only if mobile is non-null)

The first match wins. If no match is found, a new `Client` is created.

## Matching Rules

- Name match requires an exact match on **both** first_name and last_name (case-insensitive).
- Email match uses case-insensitive exact match.
- Mobile match uses exact string match (no normalization of formatting).
- Only one match per row — if a match is found via name, email is not checked.
- A matched client is **updated** with the row's data (first_name, last_name, email, mobile).
- New clients are created with `is_active=True`.

## Error Handling

| Scenario | Handling |
|----------|----------|
| Missing required column | File rejected, no rows processed |
| Row missing both email and mobile | Row skipped, counted as error |
| `email` violates UNIQUE constraint | Row skipped, counted as error |
| `mobile` violates UNIQUE constraint | Row skipped, counted as error |
| `first_name` or `last_name` empty after trim | Row skipped, counted as error |
| File exceeds 5 MB | File rejected, no rows processed |
| File has no data rows | File rejected, no rows processed |
| Encoding issues | File rejected, no rows processed |

## Output Contract

On success (some or all rows processed), the system returns:

```json
{
  "total_rows": 10,
  "created": 5,
  "updated": 3,
  "errors": 2,
  "error_details": [
    {"row": 3, "message": "At least one of email or mobile is required."},
    {"row": 7, "message": "Client with this email already exists."}
  ]
}
```

This is rendered in the Django template; the JSON structure is the internal contract between the CSV processor and the view.
