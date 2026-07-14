# Auto-set date on class slot selection

## User story

As a system user, I want when selecting a "Bloque de clase" on the reservation create page, the date to be automatically set to the corresponding day, so that I can eliminate date capture errors.

## Acceptance criteria

Given I'm creating a new reservation, when I select a class slot, then the date field is automatically set to the closest future occurrence of that day where no class on that day has already started, or start later on that day.

Given I'm creating a new reservation, when I change the selected class slot, then the date field recalculates automatically.

Given I'm creating a new reservation, when the date was auto-filled, then I can still manually override it.

Given I'm creating a new reservation, when no class slot is selected, then the date field stays unmodified.

## Logic

The auto-date follows this calculation:

- If the class slot's day-of-week matches today AND the current time is **before the earliest class time** on that day → **next week** (skip all same-day slots).
- If the class slot's day-of-week matches today AND the current time is **past any class time** on that day → **next week** (skip all same-day slots).
- If the class slot's day-of-week is a **different future day** this week → **that day** this week.
- If the class slot's day-of-week is a **past day** this week → **that day** next week.

The day-of-week mapping supports 0=Monday through 6=Sunday (future-proof for Saturday/Sunday classes).

## Examples

| Today | Time | Selected class | Auto-date | Reason |
|-------|------|---------------|-----------|--------|
| Mon Jul 13 | 10:00 | Wed 17:30 | Jul 15 Wed | Next Wednesday, still ahead |
| Tue Jul 14 | 14:00 | Tue 17:30 | Jul 21 Tue | Today, today's classes haven't
started, but can't be reserved → skip all Tue |
| Tue Jul 14 | 17:40 | Tue 17:30 | Jul 21 Tue | Today, but Tue 17:30 already started → skip all Tue |
| Tue Jul 14 | 17:40 | Tue 18:29 | Jul 21 Tue | Today, but Tue 17:30 already started → skip all Tue |
| Wed Jul 15 | 18:35 | Wed 17:30 | Jul 22 Wed | Today, but all Wed classes already passed |

## Definition of Done

Code reviewed, tested with multiple time zones and day boundaries, validated against the examples table above.
