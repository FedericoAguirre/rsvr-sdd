# Research: Remove Reservations Dead Code

## Decisions

### 1. Deleted endpoint tests: remove alongside dead code

- **Decision**: Tests for the removed `/reservations/list/` endpoint will be deleted.
- **Rationale**: Keeping dead tests creates maintenance burden and CI noise. The main `/reservations/` endpoint behavior is covered by remaining test classes.
- **Alternatives considered**: Keeping and adapting tests to the main endpoint (unnecessary since main endpoint already has coverage).

### 2. Ghost migration: complete it properly

- **Decision**: Create migration `0004_add_updated_by.py` instead of just deleting the orphaned `.pyc`.
- **Rationale**: Complements existing `created_by` and `updated_at` fields, completing abandoned work at negligible effort.
- **Alternatives considered**: Simply deleting the `.pyc` artifact (loses a useful model improvement).

### 3. PDF export URL: relocate to `/reservations/pdf/`

- **Decision**: Move from `/reservations/list/pdf/` to `/reservations/pdf/`.
- **Rationale**: The `list/` parent path is being removed; PDF export should live under the main reservations namespace.
- **Alternatives considered**: Keeping at `/reservations/list/pdf/` (would require keeping a dead parent route).
