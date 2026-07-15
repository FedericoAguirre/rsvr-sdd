# Research: Auto-set Date on Class Slot Selection

## Existing Form Structure

- **URL**: `GET /reservations/create/`
- **View**: `reservation_create` (function-based, `backend/apps/reservations/views.py:173`)
- **Form**: `ReservationForm` (`backend/apps/reservations/forms.py`)
  - `class_slot`: `<select class="form-control">` — populated with active ClassSlot records
  - `date`: `<input type="date" class="form-control">`
- **Template**: `backend/apps/reservations/templates/reservations/reservation_form.html`
  - Iterates over fields generically with `{% for field in form %}`
  - Each field in `col-md-6` wrapper

## ClassSlot Model

- `day_of_week`: IntegerField (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri)
- `time`: TimeField (e.g., 17:30, 18:30)
- `is_active`: BooleanField
- No `end_time` — single `time` is the start time
- `unique_together = ["day_of_week", "time"]`

## Auto-Date Algorithm (from spec)

1. If today matches class slot's day-of-week AND current time is before **any** class time on that day → next week (skip all same-day)
2. If today matches class slot's day-of-week AND current time is past any class time on that day → next week
3. If class slot's day-of-week is a different **future** day this week → that day this week
4. If class slot's day-of-week is a **past** day this week → that day next week

## Decision: Pure Vanilla JS

- No jQuery or htmx needed — simple DOM event listener on the class_slot `<select>`
- Calculate date using `Date` object and day-of-week math
- Set the `<input type="date">` value to the calculated ISO date
- Server-side duplicates the logic for validation on form submit
