# Quickstart: Auto-set Date on Class Slot Selection

## Implementation Steps

### Step 1: Expose class slot data to template

In `backend/apps/reservations/views.py`, add all active class slots to the template context as JSON:

```python
from django.core.serializers import serialize
from apps.classes.models import ClassSlot

slots = ClassSlot.objects.filter(is_active=True).values("id", "day_of_week", "time")
context = {"form": form, "class_slots_json": json.dumps(list(slots))}
```

### Step 2: Create JS file

Create `backend/apps/reservations/static/reservations/js/auto-date.js` with the calculation logic.

### Step 3: Add JS to template

In `backend/apps/reservations/templates/reservations/reservation_form.html`, add:

```html
{{ class_slots_json|json_script:"class-slots-data" }}
<script src="{% static 'reservations/js/auto-date.js' %}"></script>
```

### Step 4: Write tests

Add Python tests in `backend/tests/test_reservations.py` for the server-side calculation logic.

### Step 5: Run tests

```bash
docker compose exec web uv run pytest tests/ -v
```
