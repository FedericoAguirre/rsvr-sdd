# Research: Update Auto-Date Algorithm

## Existing Implementation Summary

The auto-date feature (from feature 041) consists of two parallel implementations:

### 1. Client-Side: `backend/apps/reservations/static/reservations/js/auto-date.js`

Current logic calculates days ahead with three cases:
- **Same day-of-week**: +7 days (next week) — ✅ keep
- **Past day (earlier this week)**: wrap to next week — ✅ keep
- **Future day (later this week)**: days until that day this week — ❌ change to +7

### 2. Server-Side: `backend/apps/reservations/views.py` — `auto_date_for_slot()`

Mirrors the JS algorithm with identical logic. Same three cases.

### 3. Tests: `backend/tests/test_reservations.py` — `TestAutoDate`

Five test methods that assert specific date outputs:
- `test_same_day_goes_to_next_week` — asserts 7 days ahead
- `test_future_day_this_week` — asserts this-week date for future day **❌ will change**
- `test_past_day_goes_to_next_week` — asserts next-week date for past day
- `test_invalid_slot_returns_none` — asserts None for invalid slot
- `test_same_day_always_goes_to_next_week` — asserts 7 days regardless of time

## Required Changes

### Algorithm Change

The only change needed: for a future day later this week, add 7 to push to next week instead of selecting this week.

**New JS logic:**
```javascript
var daysAhead = slotDay - todayDay;
if (daysAhead <= 0) {
    daysAhead += 7;  // Same day or past day → next week
} else {
    daysAhead += 7;  // Future day → next week, not this week
}
```

Equivalent simplified form: `daysAhead = (slotDay - todayDay + 14) % 7 + 7`

**New Python logic (views.py):**
```python
days_ahead = slot_day - today_day
if days_ahead <= 0:
    days_ahead += 7  # Same or past
else:
    days_ahead += 7  # Future → next week
```

### Test Changes

`test_future_day_this_week` needs its expected assertion changed: the future day should now resolve to the same day-of-week in the following week (diff + 7).

## Decision

- **No new dependencies required** — pure algorithm change
- **No data migration needed** — only affects new reservations
- **No template changes needed** — HTML/CSS unchanged
- **No i18n changes needed** — no new user-visible strings
