# Quickstart: Switch Date and Class Block Columns

## What To Change

1. Open `backend/apps/clients/templates/clients/client_detail.html`
2. In the `<thead>` section, reorder the three `<th>` elements from:
   - `Date`, `Class`, `Equipment` → `Class`, `Date`, `Equipment`
3. In the `<tbody>` section, reorder the three `<td>` elements correspondingly:
   - `r.date`, `r.class_slot`, `r.equipment` → `r.class_slot`, `r.date`, `r.equipment`

## What To Test

1. Create a simple test that loads the client detail page and verifies the HTML column order
2. Run: `docker compose exec web uv run pytest backend/tests/test_client_detail.py -v`

## What NOT To Change

- No CSS files
- No JavaScript files
- No Python views or models
- No translation files (i18n)
- No migration files
