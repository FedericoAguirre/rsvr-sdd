# Quickstart: Rename Exported Reservations PDF

## Scope

Single-file change to `backend/apps/reservations/views.py` in the
`reservation_list_pdf` view function.

## Required Change

In `views.py`, update the `Content-Disposition` header from:

```python
response["Content-Disposition"] = f'attachment; filename="reservations-{date_str}.pdf"'
```

to:

```python
safe_name = class_slot.name.replace(" ", "_").translate(str.maketrans("", "", r'/\0<>:"|?*'))
date_compact = date_str.replace("-", "")
response["Content-Disposition"] = f'attachment; filename="reservations_{safe_name}_{date_compact}.pdf"'
```

## Fallback Handling

- If `date_str` is empty: use `"no_date"` instead of date compact
- If `class_slot` is None: use `"unknown"` instead of safe_name
- If both are missing: use `"reservations_export.pdf"`

## Testing

Update assertions in `backend/tests/test_reservations_list.py` that verify
the `Content-Disposition` header to match the new format.
