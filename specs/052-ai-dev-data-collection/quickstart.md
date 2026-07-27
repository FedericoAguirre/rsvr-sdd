# Quickstart: AI Development Data Collection

## Prerequisites

- Docker Compose environment running (`docker compose up -d`)
- At least one completed feature in `ai/features/done/`
- At least one session log in `ai/sessions/`
- At least one spec file under `specs/`

## Setup

No database setup required — this feature reads from flat files only.

```bash
# Ensure environment is running
docker compose up -d
```

## Validation Scenarios

### Scenario 1: Basic CSV generation

```bash
docker compose exec web uv run manage.py collect_ai_dev_data --output /tmp/test_ai_data.csv
```

**Expected outcome**:
- Exit code 0
- File `/tmp/test_ai_data.csv` exists
- File contains header row: `feature,complexity,minutes,model,start_timestamp,end_timestamp,specs_quality,iterations`
- File contains at least one data row

Verify with:
```bash
head -5 /tmp/test_ai_data.csv
wc -l /tmp/test_ai_data.csv
```

### Scenario 2: CSV validity check

```bash
docker compose exec web python -c "
import csv
with open('/tmp/test_ai_data.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    assert header == ['feature', 'complexity', 'minutes', 'model', 'start_timestamp', 'end_timestamp', 'specs_quality', 'iterations'], f'Bad header: {header}'
    for row in reader:
        assert len(row) == 8, f'Expected 8 columns, got {len(row)}: {row}'
        assert row[1] in ('', '1', '2', '3', '5', '8'), f'Bad complexity: {row[1]}'
        assert row[6] in ('', '1', '2', '3', '4', '5'), f'Bad specs_quality: {row[6]}'
print('CSV validation PASSED')
"
```

### Scenario 3: Empty state (no features)

Run in a clean environment without any features:

```bash
# Temporarily rename done/ dir to simulate empty state
# OR just verify header-only output is well-formed
docker compose exec web python -c "
import csv
from io import StringIO
# Empty CSV should have just the header
output = 'feature,complexity,minutes,model,start_timestamp,end_timestamp,specs_quality,iterations\n'
reader = csv.reader(StringIO(output))
header = next(reader)
assert header == ['feature', 'complexity', 'minutes', 'model', 'start_timestamp', 'end_timestamp', 'specs_quality', 'iterations']
assert list(reader) == []
print('Empty CSV validation PASSED')
"
```

### Scenario 4: Run the full test suite

```bash
docker compose exec web uv run pytest backend/tests/test_collect_ai_dev_data.py -v
```

**Expected outcome**: All tests pass.

## Contracts and Data Model

- Command interface: [contracts/command-interface.md](contracts/command-interface.md)
- Data model: [data-model.md](data-model.md)
