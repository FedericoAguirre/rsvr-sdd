# Quickstart: Add ClassPrice Sub-Option Under "Horario" Menu

## Prerequisites

- Project running (`uv run python manage.py runserver` or Docker)
- At least one user with `classes.view_classslot` permission (e.g., a staff user via admin)
- At least one ClassPrice record (to verify the page renders)

## Validation Steps

### 1. Apply the template change

In `backend/templates/base.html`, replace the flat "Horario" link (line 28):

```html
<li class="nav-item"><a class="nav-link" href="{% url 'classes:class-schedule' %}">{% translate "Schedule" %}</a></li>
```

With a dropdown:

```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">{% translate "Schedule" %}</a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{% url 'classes:class-schedule' %}">{% translate "Class Schedule" %}</a></li>
        <li><a class="dropdown-item" href="{% url 'classes:price-list' %}">{% translate "Class prices" %}</a></li>
    </ul>
</li>
```

### 2. Verify the dropdown appears (desktop)

1. Start the development server: `cd backend && uv run python manage.py runserver`
2. Open `http://localhost:8000/accounts/login/` in a browser
3. Log in as a user with `classes.view_classslot` permission
4. **Expected**: "Horario" appears in the nav bar. Click it — a dropdown opens with two items:
   - "Horario de Clases"
   - "Precios de clase"

### 3. Verify each link navigates correctly

1. Click "Horario de Clases" → **Expected**: navigates to `/classes/` showing the schedule table
2. Navigate back, click "Horario" dropdown again
3. Click "Precios de clase" → **Expected**: navigates to `/classes/prices/` showing the price list

### 4. Verify permission gate

1. Log in as a user without `classes.view_classslot` permission
2. **Expected**: No "Horario" menu item is visible at all

### 5. Verify mobile responsiveness

1. Resize browser to < 992px width
2. **Expected**: Nav collapses into hamburger menu. Expand it — "Horario" shows as a dropdown toggle. Both sub-items are accessible.

### 6. Run the test suite

```bash
cd backend && uv run pytest
```

**Expected**: All existing tests pass. No regressions.

### 7. Verify Docker (optional)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-build web
docker exec rsvr-sdd-web-1 uv run python manage.py check
```

**Expected**: Zero warnings.
