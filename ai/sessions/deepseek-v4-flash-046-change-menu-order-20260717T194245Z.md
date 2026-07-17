# Session: Change navigation bar menu order

**Branch**: `046-change-menu-order`
**Model**: deepseek-v4-flash

## Work Done

- Reordered navigation bar menu items in `backend/templates/base.html` from (Reservations, Clients, Equipment, Schedule, Payments, Reports, Admin, Logout) to desktop workflow order: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión
- TDD test written first (`test_navbar_menu_item_order` in `tests/test_i18n.py`) — confirmed RED, then GREEN after reorder
- All existing i18n tests continue to pass unchanged
- No i18n changes needed — all labels already used `{% translate %}`

## Tests

1 new test in `tests/test_i18n.py`:
- `test_navbar_menu_item_order`: Renders any authenticated page, extracts nav links by `nav-link` class in document order, asserts full 8-item menu sequence

## Total Test Count

**225 passed, 9 pre-existing failures** (same 9 unrelated failures as before)

## Files Changed

- `backend/templates/base.html:17-40` — reordered `<li>` elements to: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión
- `backend/tests/test_i18n.py` — added `_extract_nav_items()` helper + `test_navbar_menu_item_order` test
- `specs/046-change-menu-order/tasks.md` — task tracking

## Spec Artifacts

`specs/046-change-menu-order/` — spec.md, plan.md, tasks.md, research.md, data-model.md, quickstart.md, checklists/requirements.md (all complete)
