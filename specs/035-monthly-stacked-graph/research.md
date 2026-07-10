# Research: Monthly Stacked Graph

## Technical Investigation

### 1. Date Snapping Logic

- **Goal**: Snap start date to 1st of month, end date to last day of month.
- **Approach**: Pure Python `datetime.date` arithmetic — same pattern as weekly (`034`).
  - Start: `start_dt = start_dt.replace(day=1)`
  - End: Use `calendar.monthrange(year, month)` to get last day, then `end_dt = end_dt.replace(day=last_day)`.
- **Edge cases**: February (28/29), months with 30 days. `calendar.monthrange` handles all correctly.
- **Input field update**: Snapped values written to `start_date` / `end_date` in context — template reads these for input `value=`, same as existing week snapping.

### 2. Frontend YYYYMM Labels

- **Current monthly code** (`views.py:242-244`): Returns `date__year` and `date__month` fields separately.
- **Label formatting**: In `formatLabel()` template function, when `r.date__year` and `r.date__month` are present, format as `${r.date__year}${String(r.date__month).padStart(2, '0')}` (e.g., `202607`).
- **Detection**: No need for a new flag — check for `r.date__month` presence (distinct from `r.date` / `r.week`) in the `formatLabel` function.

### 3. Existing Infrastructure

- Monthly grouping already exists in `PaymentReportView` (lines 241-244) using `date__year`, `date__month`.
- No query changes needed — only snapping + label format.
- Responsive/gridlines configuration already applied globally via Chart.js options.

### 4. i18n Impact

- No new user-facing strings. "Month" dropdown option already exists.
- Error messages ("No payment data for the selected period.", "Failed to load chart data.") already translated from prior work.
