# Quickstart: Change navigation bar menu order

## Implementation Steps

1. **Write TDD test** (before changing template):
   - Add a test to `backend/tests/test_i18n.py` that renders a page and asserts nav `<li>` items appear in the specified left-to-right order (Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión)
   - Run: `docker compose exec web uv run manage.py test backend.tests.test_i18n --verbosity=2`
   - Confirm the new test **fails** (red)

2. **Reorder template**:
   - Edit `backend/templates/base.html` lines 17-40
   - Move each `<li>` block (including its `{% if %}` wrapper where applicable) to match the target order
   - Ensure the Logout `<li>` (lines 35-40, form with button) moves as a complete block

3. **Verify**:
   - Re-run the test: confirm **passes** (green)
   - Run full suite: `docker compose exec web uv run manage.py test --verbosity=2`
   - Manually check the nav renders correctly at desktop and mobile widths

## Test Commands

```bash
# Single test
docker compose exec web uv run manage.py test backend.tests.test_i18n --verbosity=2

# Full suite
docker compose exec web uv run manage.py test --verbosity=2
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/templates/base.html` | Navbar definition (sole file to change) |
| `backend/tests/test_i18n.py` | Existing + new nav order tests |
