# Data Model: Batch Reservation Weekly Date Groups

## Overview

No backend data model changes. This feature modifies only the client-side rendering of date data already returned by `BatchDataView`. The data model below describes the JavaScript-side data structures used by `renderBatchForm()`.

---

## Input: Backend JSON (`BatchDataView` response — unchanged)

```json
{
  "date_range": { "start": "2026-01-15", "end": "2026-02-09" },
  "block_class_count": 4,
  "payment_id": 42,
  "equipment_list": [ { "id": 1, "name": "Bicicleta" } ],
  "class_slots": [ { "id": 3, "label": "Mañana (9:00)", "day_of_week": 0 } ],
  "reserved_dates": [ "2026-01-22" ]
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `date_range.start` | ISO date string | First available date (a Monday) |
| `date_range.end` | ISO date string | Last available date (4 weeks later, a Friday) |
| `block_class_count` | integer | Number of dates user must select (max 20) |
| `reserved_dates` | string[] | ISO dates where client already has a reservation (excluded from buttons) |

---

## Client-Side Date Processing (unchanged logic)

1. Iterate from `date_range.start` to `date_range.end`
2. Skip weekends (ISO weekday >= 5)
3. Skip dates present in `reserved_dates`
4. For each valid date, create a button with `data-date` and `data-dow` attributes

---

## New: Weekly Grouping (added by this feature)

The flat list of date buttons is grouped into weeks of 5 consecutive dates:

```
Week group:
  ├── Header row: 5 day-of-week labels (Lun, Mar, Mié, Jue, Vie)
  └── Date row:   5 date buttons (Mon–Fri with no gaps)
```

### Grouping Algorithm

```
dates = sorted(valid_dates)  # already chronological
weeks = []
for i in range(0, len(dates), 5):
    week_group = dates[i:i+5]  # exactly 5 dates per group
    weeks.append(week_group)
```

### Assumptions

- `date_range.start` is always a Monday (guaranteed by existing backend logic)
- All dates within the 4-week range are consecutive Monday–Friday (no gaps)
- Exactly 20 valid dates (4 weeks × 5 days) after excluding reserved dates
- If fewer than 20 dates are available (e.g., a reserved date creates a hole), the partial week renders with fewer buttons — column alignment is maintained by CSS grid

---

## UI DOM Structure

```html
<div id="dateList" class="batch-date-grid">
  <!-- Week group 1 -->
  <div class="week-group">
    <div class="week-header">
      <span class="day-label">Lun</span>
      <span class="day-label">Mar</span>
      <span class="day-label">Mié</span>
      <span class="day-label">Jue</span>
      <span class="day-label">Vie</span>
    </div>
    <div class="week-row">
      <button class="btn btn-outline-secondary btn-sm date-btn" data-date="2026-01-15" data-dow="0">15/1</button>
      <button class="btn btn-outline-secondary btn-sm date-btn" data-date="2026-01-16" data-dow="1">16/1</button>
      ...
    </div>
  </div>
  <hr class="week-separator">
  <!-- Week group 2... same structure -->
</div>
```

### CSS Grid for `.week-row`

```css
.week-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}
.week-header {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}
```

This ensures 5 equal columns with headers aligned to date buttons.

---

## State Transitions

No state transitions — the date data is rendered once when the modal loads and selection state is managed by `toggleDate()` (unchanged). The weekly grid is a pure visual transformation of the existing flat date list.
