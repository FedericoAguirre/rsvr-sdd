# Command Interface: AI Development Data Collection

## Management Command: `collect_ai_dev_data`

**Location**: `backend/apps/reservations/management/commands/collect_ai_dev_data.py`

**Base class**: `django.core.management.base.BaseCommand`

### Usage

```bash
docker compose exec web uv run manage.py collect_ai_dev_data [--output PATH]
```

### Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--output`, `-o` | path | `./ai_dev_data.csv` | Output file path for the generated CSV |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — CSV generated |
| 1 | Error — unexpected failure (logged to stderr) |

### Output

The command writes a CSV file (RFC 4180) to the specified path with the following columns and no BOM:

```
feature,complexity,minutes,model,start_timestamp,end_timestamp,specs_quality,iterations
"Track Developer Invested Time (CSV Export)",2,45,deepseek-v4-flash-free,2026-07-12T02:01:57Z,2026-07-12T03:00:00Z,4,3
```

### Output Format Constraints

- Header row is always present (even if no data rows)
- Fields containing commas, newlines, or double-quotes are escaped per RFC 4180
- Empty fields are represented as empty strings (e.g., `,`, between commas)
- Timestamps use ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`)
- Line endings: LF (`\n`)
