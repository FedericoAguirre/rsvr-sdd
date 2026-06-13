# Quickstart: Client List Feature

## What It Does

When an Operator navigates to `clients/search/`, they see:
1. A **search form** (existing) — search by email or mobile
2. A **pagination client list** (new) — all clients displayed with all attributes
3. A **counter widget** (existing, now always visible) — total number of clients
4. An **Edit button** per row (new) — navigates to the admin change form

If no clients exist, an empty state message is shown.
If more than 10 clients exist, pagination controls appear at the bottom of the list.

## How to Verify

1. Create 15+ clients via seed or admin
2. Navigate to `clients/search/`
3. Confirm all 15 clients are visible across pages (10 on page 1, 5 on page 2)
4. Confirm all attributes (name, email, mobile, active status, dates) display
5. Confirm the counter shows "15"
6. Click Edit on any row — confirm it opens the admin change form for that client
7. Enter a search query — confirm the list filters to matching clients (paginated if >10)
8. Clear the search — confirm the full list reappears
9. Delete all clients — confirm the empty state message appears

## Commands

```bash
# Create test clients
python manage.py seed 21  # requires seed command or manual creation

# Run tests
pytest backend/tests/test_client_list.py -v
```
