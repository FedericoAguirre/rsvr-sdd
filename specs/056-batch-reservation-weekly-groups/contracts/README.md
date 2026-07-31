# Contracts: Batch Reservation Weekly Date Groups

## UI Contract

The batch reservation modal renderer (`renderBatchForm()` in `payment_detail.html`) is the single frontend contract for this feature. It defines:

1. **Date rendering**: 20 dates grouped into 4 weekly rows of 5 days each (Mon–Fri), displayed as a CSS Grid with day-of-week column headers.
2. **Day labels**: 3-letter Spanish abbreviations (Lun, Mar, Mié, Jue, Vie) localized via Django `json_script` and i18n.
3. **Date format**: Short `DD/M` format within buttons (e.g., "15/1", "1/2").
4. **Visual grouping**: `<hr>` separators between week groups with reduced opacity.
5. **Selection state**: Active buttons use Bootstrap `.btn-primary`; inactive use `.btn-outline-secondary` (unchanged).

### Contract Invariants (Must Not Change)

- `data-date` and `data-dow` attributes on each date button must be preserved.
- `toggleDate()` function must work identically — click toggles selection state.
- `submitBatch()` must receive the same date format (ISO strings in an array).
- Hidden checkboxes are not used — selection is tracked via `selectedDates` JS object.
- The `#dateCount` element must update in real-time with selection count.
- The "Create Reservations" button must remain disabled when no dates are selected.

### Responsive Behavior

| Viewport | Grid Layout | Scrolling |
|----------|-------------|-----------|
| Desktop >= 1024px | 5-column grid, all dates visible | `.modal-dialog-scrollable` if content exceeds modal height |
| Tablet 768–1024px | 5-column grid preserved | Modal body scrolls vertically |
| Mobile < 768px | 5-column grid preserved, tighter spacing | Modal body scrolls vertically, no horizontal overflow |

### i18n Contract

The following user-visible strings must be internationalized:

| String | Current (hardcoded) | New (i18n) |
|--------|---------------------|------------|
| Day abbreviation Mon | `DAY_ABBRS[0] = "L"` | `"Lun"` via `{% translate %}` |
| Day abbreviation Tue | `DAY_ABBRS[1] = "M"` | `"Mar"` via `{% translate %}` |
| Day abbreviation Wed | `DAY_ABBRS[2] = "X"` | `"Mié"` via `{% translate %}` |
| Day abbreviation Thu | `DAY_ABBRS[3] = "J"` | `"Jue"` via `{% translate %}` |
| Day abbreviation Fri | `DAY_ABBRS[4] = "V"` | `"Vie"` via `{% translate %}` |
| Day abbreviation Sat | `DAY_ABBRS[5] = "S"` | `"Sáb"` via `{% translate %}` |
| Day abbreviation Sun | `DAY_ABBRS[6] = "D"` | `"Dom"` via `{% translate %}` |
