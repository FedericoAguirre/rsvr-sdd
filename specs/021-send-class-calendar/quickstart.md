# Quickstart: Send Class Reservations Calendar to Client

## Setup

### 1. Add icalendar dependency

```bash
cd backend
uv add icalendar>=5.0
```

### 2. Update `backend/apps/clients/urls.py`

Add calendar route:
```python
path("<int:pk>/calendar/", views.client_calendar, name="client-calendar"),
```

### 3. Add view in `backend/apps/clients/views.py`

Add `client_calendar` view that:
- Accepts `start_date` and `end_date` GET parameters
- Validates the date range
- Queries reservations for the client within the range
- Generates an ICS file using `icalendar`
- Returns the file as an HTTP attachment response

### 4. Update template `backend/apps/clients/templates/clients/client_detail.html`

Add:
- A date range form (start date + end date inputs)
- A "Download Calendar" button submitting to `{% url 'clients:client-calendar' client.pk %}`
- Error/empty-state message area

### 5. Add translations

```bash
cd backend
django-admin makemessages -l es
# Edit locale/es/LC_MESSAGES/django.po with new strings
django-admin compilemessages
```

## Testing

### Run existing tests to confirm no regressions

```bash
cd backend
uv run pytest
```

### Test new feature

```bash
cd backend
uv run pytest tests/test_client_calendar.py -v
```

### Manual test

1. Navigate to a client detail page
2. Select a date range with reservations
3. Click "Download Calendar"
4. Open the ICS file in a calendar application
5. Verify events contain correct data

## Key Files

| File | Action |
|------|--------|
| `backend/apps/clients/urls.py` | Add route |
| `backend/apps/clients/views.py` | Add view |
| `backend/apps/clients/templates/clients/client_detail.html` | Add form + button |
| `backend/tests/test_client_calendar.py` | New test file |
| `backend/pyproject.toml` / `uv.lock` | Updated with icalendar |
