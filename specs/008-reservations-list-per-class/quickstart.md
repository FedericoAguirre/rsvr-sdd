# Quickstart: Create Reservations List per Class Slot

## Setup

```bash
cd backend

# Install WeasyPrint system dependencies (required for PDF generation)
sudo apt-get install -y libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0

# Install Python dependencies
pip install weasyprint

# Apply any pending migrations
python manage.py migrate
```

## Verification

```bash
# Open the reservations list for a specific class slot and date
# e.g., class_slot=1, date=2026-06-15
open http://localhost:8000/reservations/list/?class_slot=1&date=2026-06-15
```

Expected: A page showing the date and class slot name in the header, with a table of equipment names and client names ordered alphabetically.

```bash
# Test PDF export
open http://localhost:8000/reservations/list/pdf/?class_slot=1&date=2026-06-15
```

Expected: A PDF file downloads containing the same information.

```bash
# Empty state
open http://localhost:8000/reservations/list/?class_slot=1&date=2099-01-01
```

Expected: Header shown with an empty table and a "No reservations" message.

## Tests

```bash
cd backend
.venv/bin/python -m pytest tests/ -v -k "reservation"
```

Expected: All reservation-related tests pass, including new list view and PDF export tests.
