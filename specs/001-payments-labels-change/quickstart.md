# Quickstart: Payments Labels Change

## Files to Modify

| File | Change |
|------|--------|
| `backend/apps/payments/templates/payments/payment_list.html` | Replace labels, placeholders, and button CSS classes |
| `backend/locale/es/LC_MESSAGES/django.po` | Remove unused `"Search by Client"` entry, add new usage comment for `"Search clients..."` |
| `backend/locale/es/LC_MESSAGES/django.mo` | Recompile after PO changes |
| `backend/tests/test_payments_search.py` | Update assertions for new labels/classes |

## Implementation Steps

### Step 1: Update `payment_list.html` (4 changes)

**Change 1** — Label for search field (line 23):
- Old: `{% translate "Search by Client" %}`
- New: `{% translate "Search Clients" %}`

**Change 2** — Placeholder for search input (line 24):
- Old: `placeholder="{% translate 'Search by client name, email or mobile...' %}"`
- New: `placeholder="{% translate 'Search clients...' %}"`

**Change 3** — Filter button (line 27):
- Old: `<button type="submit" class="btn btn-outline-secondary">`
- New: `<button type="submit" class="btn btn-primary">`

**Change 4** — "New Payment" button (line 10):
- Old: `<a href="..." class="btn btn-primary">`
- New: `<a href="..." class="btn btn-success">`

### Step 2: Update i18n

```sh
cd backend
uv run django-admin makemessages --all        # Update PO file with new references
# Edit locale/es/LC_MESSAGES/django.po to remove unused "Search by Client" entry
uv run django-admin compilemessages              # Regenerate .mo file
```

### Step 3: Update Tests

Update assertions in `backend/tests/test_payments_search.py`:
- Verify the search label uses `"Search Clients"` (renders as `"Buscar Clientes"`)
- Verify the search placeholder uses `"Search clients..."` (renders as `"Buscar clientes..."`)
- Verify the search button has class `btn-primary`
- Verify the "New Payment" button has class `btn-success`

### Step 4: Verify

```sh
docker compose run --rm web uv run pytest backend/tests/ -v -k "payment"
```
