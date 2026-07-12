# Session: Journal Minutes Column

**Branch**: `037-developer-time-tracking`
**Model**: deepseek-v4-flash-free

## Work Done

- Added `Journal Minutes` column to `scripts/developer-time.sh` — raw wall-clock span `(last_ts - first_ts) / 60` per developer/date group, without gap detection
- Column placed after `Last Commit`, before `Minutes`, so both the gap-aware and raw-span metrics appear side by side
- Updated test fixture (`test/fixtures/test-repo.sh`) with expected values — all 6/6 tests pass
- Updated contract docs (`specs/037-developer-time-tracking/contracts/cli.md`) with new column

## Files Modified

- `scripts/developer-time.sh` — Journal Minutes column added to header, computation, and both `printf` calls
- `test/fixtures/test-repo.sh` — all 4 data rows updated with `journal_min` value
- `specs/037-developer-time-tracking/contracts/cli.md` — example output and column description updated

## Spec Artifacts

`specs/037-developer-time-tracking/` — spec.md, plan.md, research.md, data-model.md, quickstart.md, contracts/ (all complete)
