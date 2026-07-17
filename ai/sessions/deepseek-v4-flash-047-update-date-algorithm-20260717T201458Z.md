# Session: Update Auto-Date Algorithm

**Branch**: `047-update-date-algorithm`
**Model**: deepseek-v4-flash

## Work Done

- Changed auto-date algorithm from time-based to always-next-week: selecting any class slot always sets the date to the same day-of-week in the following week
- **JS** (`backend/apps/reservations/static/reservations/js/auto-date.js`): simplified `autoDate()` to `daysAhead = slotDay - todayDay + 7`
- **Python** (`backend/apps/reservations/views.py`): simplified `auto_date_for_slot()` to `days_ahead = slot_day - today_day + 7`
- **Test** (`backend/tests/test_reservations.py`): updated `test_future_day_this_week` → `test_future_day_goes_to_next_week` with frozen-date assertion (expected diff 9 for Mon→Wed selection)

## Algorithm Change

**Old**: future day later this week → this week; same/past → next week
**New**: always → same day-of-week in the following week (`slot_day - today_day + 7`)

## Tests

| Test | Status |
|------|--------|
| `test_same_day_goes_to_next_week` (T001) | ✅ PASS |
| `test_future_day_goes_to_next_week` (T002) | ✅ PASS |
| `test_past_day_goes_to_next_week` (T003) | ✅ PASS |
| `test_invalid_slot_returns_none` (T004) | ✅ PASS |
| `test_same_day_always_goes_to_next_week` (T008) | ❌ Pre-existing failure (missing fixture) |

## Files Changed

- `backend/apps/reservations/static/reservations/js/auto-date.js` — algorithm simplification
- `backend/apps/reservations/views.py` — algorithm simplification
- `backend/tests/test_reservations.py` — updated test assertion + frozen-date mock
- `specs/047-update-date-algorithm/tasks.md` — task tracking

## Spec Artifacts

`specs/047-update-date-algorithm/` — spec.md, plan.md, tasks.md, research.md, data-model.md, quickstart.md, checklists/requirements.md
