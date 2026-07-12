# Quickstart: ReportLab Migration

## Add ReportLab dependency

```bash
docker compose exec web uv add reportlab>=4.0
```

## Remove WeasyPrint dependency

```bash
docker compose exec web uv remove weasyprint
```

## Update Dockerfile

Remove these lines from `backend/Dockerfile`:

```
libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0
```

## Run tests

```bash
docker compose exec web uv run manage.py test backend.tests.test_reservations_list
```

## Verify PDF generation

1. Navigate to Reservations → select a class slot and date
2. Click "Export PDF" button
3. Verify PDF downloads with correct filename
4. Open PDF and verify: title, date, class name, table with borders, reservation data
5. Test empty state: select a class/date with no reservations — verify "No reservations" message

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ImportError: No module named reportlab` | Run `uv add reportlab>=4.0` |
| Missing i18n strings | Check `backend/locale/es/LC_MESSAGES/django.po` for missing translation keys |
| PDF not downloading | Check browser popup blocker; verify view exception handling |
