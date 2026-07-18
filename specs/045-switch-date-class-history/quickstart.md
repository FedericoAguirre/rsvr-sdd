# Quickstart: Switch date and class block columns in history

## Prerequisites

- Docker environment running (`make up` or `docker compose up -d`)
- Feature branch checked out: `045-switch-date-class-history`

## Implementation Steps

### 1. Write TDD tests (WRITE FIRST — expect them to FAIL)

Create/update `backend/tests/test_client_detail.py` with a test that checks column order in the `<thead>` of the "Historial de Reservas" table on `clients/{id}/`.

```python
# Expected column order: Clase, Fecha, Equipo
```

### 2. Verify tests fail

```sh
docker compose exec web uv run pytest backend/tests/test_client_detail.py -v -k "test_columns_in_correct_order"
```

### 3. Reorder template columns

Edit `backend/apps/clients/templates/clients/client_detail.html`:
- Move `<th>{% translate "Class" %}</th>` and `<td>{{ r.class_slot }}</td>` before the Date column
- Resulting order: Class, Date, Equipment

### 4. Verify tests pass

```sh
docker compose exec web uv run pytest backend/tests/test_client_detail.py -v
```

### 5. Full test suite

```sh
docker compose exec web uv run pytest
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/apps/clients/templates/clients/client_detail.html` | Single template change |
| `backend/tests/test_client_detail.py` | TDD tests |
| `specs/045-switch-date-class-history/` | Spec and plan artifacts |
