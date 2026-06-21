# Quickstart: CSV Client Upload

## Development Setup

1. Ensure you are on the `016-csv-client-upload` branch.

2. Activate the Python environment and install any new dependencies (none expected — uses Python stdlib `csv`).

3. Add the CSV upload view, form, and URL pattern:
   - `backend/apps/clients/csv_import.py` — CSV parsing, matching, and processing logic
   - `backend/apps/clients/forms.py` — add `ClientCsvUploadForm`
   - `backend/apps/clients/views.py` — add `client_csv_upload` view
   - `backend/apps/clients/urls.py` — add `upload/` URL pattern
   - `backend/apps/clients/templates/clients/client_csv_upload.html` — upload page template
   - `backend/apps/clients/templates/clients/_client_csv_results.html` — results partial

4. Compile translation messages:
   ```bash
   cd backend && django-admin compilemessages
   ```

5. Run tests:
   ```bash
   cd backend && pytest tests/test_client_csv_upload.py -v
   ```

6. Run the dev server:
   ```bash
   cd backend && python manage.py runserver
   ```

7. Navigate to `/clients/upload/` to test the CSV upload.

## Test Data

A sample CSV file with valid data:

```csv
first_name,last_name,email,mobile
María,García,maria@example.com,+541112345678
Juan,Pérez,juan@example.com,+549112345679
Ana,López,ana@example.com,
Carlos,Rodríguez,,+549112345681
```

Non-breaking but edge-case CSV:

```csv
first_name,last_name,email,mobile
  María  ,  García  ,maria@example.com,+541112345678    # leading/trailing whitespace
Juan,Pérez,juan@example.com,                             # empty mobile cell
Ana,López,,+549112345680                                 # empty email cell
```
