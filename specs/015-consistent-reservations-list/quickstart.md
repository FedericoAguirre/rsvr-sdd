# Quickstart: Consistent Reservations List

## Setup

```bash
git checkout 016-consistent-reservations-list
```

## What needs to change

**Only one file requires modification:**

- `backend/apps/reservations/templates/reservations/reservation_list.html`

Optionally, for consistency in the secondary view:
- `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html`

## The Fix

In `reservation_list.html`, the table is currently wrapped in `{% if class_slot %}...{% else %}...{% endif %}`:

- **Filtered branch** (lines 42-60): renders 3 columns — Equipment, Client, Status
- **Unfiltered branch** (lines 61-77): renders 6 columns — Date, Client, Class, Equipment, Status, View

**Fix**: Remove the branching and always render the 6-column table. The filter form, date/class header, and Export PDF button remain conditional as they are.

## Verification

```bash
# Run existing tests to confirm no regressions
cd backend && python -m pytest tests/test_reservations_list.py -v
```

Key test scenarios (to be added via TDD):
1. Page loads with all 6 columns visible
2. Applying a filter shows all 6 columns (not just 3)
3. Clearing a filter restores all 6 columns
4. Export PDF remains unchanged

## Constraints

- Do NOT modify `reservation_list_pdf.html` or the PDF view
- All new/updated UI text must use i18n (`{% translate %}`)
- Tests must be written first (TDD), reviewed, and failing before implementation
