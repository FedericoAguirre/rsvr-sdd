# Contract: Auto-Date Function

## Interface

```
autoDate(classSlotValue: string, classSlots: ClassSlot[]) => string
```

- **Input**: The selected `class_slot` option value (PK), and an array of all active class slots with `day_of_week` and `time`
- **Output**: ISO date string (YYYY-MM-DD) for the calculated date

## Business Logic (pseudocode)

```
function autoDate(selectedSlotId, allSlots):
    slot = allSlots.find(s => s.id == selectedSlotId)
    today = today()
    slotDayOfWeek = slot.day_of_week  // 0=Mon..4=Fri

    // Find earliest time for this day-of-week
    sameDaySlots = allSlots.filter(s => s.day_of_week == slotDayOfWeek)
    earliestTime = min(sameDaySlots.map(s => s.time))

    // If today is the slot's day-of-week AND
    // (current time < earliestTime OR current time >= any same-day slot time)
    // → next week
    if today.getDay() - 1 == slotDayOfWeek:  // JS: Sun=0, so Mon=1..Fri=5
        if now() < earliestTime || sameDaySlots.some(s => now() >= s.time):
            return today + 7 days  // next week

    // If slot's day is still ahead this week → this week
    if slotDayOfWeek > today.getDay() - 1:
        return this week's occurrence

    // Otherwise → next week
    return next week's occurrence
```

## JS Event Binding

```javascript
document.getElementById('id_class_slot').addEventListener('change', function(e) {
    var dateInput = document.getElementById('id_date');
    dateInput.value = autoDate(e.target.value, classSlotsData);
});
```

## Data Structure

```json
[
    {"id": 1, "day_of_week": 0, "time": "17:30"},
    {"id": 2, "day_of_week": 0, "time": "18:30"},
    {"id": 3, "day_of_week": 1, "time": "17:30"}
]
```
