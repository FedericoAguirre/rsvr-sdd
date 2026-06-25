# Research: Payment Form Redesign

**Date**: 2026-06-24

## Goal

Establish the exact Django form patterns used across the project so the payment form can be brought into alignment.

## Findings

### Form Template Pattern

Every form template in the project follows this exact structure:

| Element | Standard | Payment form (current) |
|---|---|---|
| Field wrapper CSS | `col-md-6` | `col-12` |
| Button row CSS | `col-12` | `col-12` |
| Form class | `row g-3` | `row g-3` |
| Label class | `form-label` | `form-label` |
| Error display | `<div class="text-danger">{{ field.errors }}</div>` | Same |
| Help text display | `<div class="form-text">{{ field.help_text }}</div>` | Same |
| Field iteration | `{% for field in form %}` | Same |
| File upload enctype | `enctype="multipart/form-data"` | Same |

**Decision**: Change field wrapper from `col-12` to `col-md-6` to match the standard. Keep button row at `col-12`.

### Widget attrs pattern — form-control

Every reference form sets `"class": "form-control"` on all widget attrs:

- `ClientForm`: `TextInput`, `EmailInput` → `{"class": "form-control"}`
- `EquipmentForm`: `TextInput`, `Select`, `Textarea` → `{"class": "form-control"}`; `Textarea` additionally has `"rows": 3`
- `ReservationForm`: `Select`, `DateInput`, `Textarea` → `{"class": "form-control"}`; `DateInput` additionally has `"type": "date"`; `Textarea` additionally has `"rows": 3`
- CSV upload form: `FileInput` → `{"class": "form-control", "accept": ".csv"}`

The current `PaymentForm.Meta.widgets` only defines:
- `date`: `DateInput(attrs={"type": "date"})` — **missing** `"class": "form-control"`
- `notes`: `Textarea(attrs={"rows": 3})` — **missing** `"class": "form-control"`

No widgets are defined for: `client`, `amount`, `payment_type`, `payment_identifier`, `class_slot_count`, `reference`, `evidence`.

**Decision**: Add `"class": "form-control"` to all existing widget definitions and define new widget entries for all remaining fields. For the `evidence` field (ImageField), use `forms.FileInput(attrs={"class": "form-control"})` matching the csv_upload form pattern.

### Testing approach

**Decision** per Constitution Gate 1 (TDD):

- **FR-003 test**: Write a unit test `test_all_widgets_have_form_control` that iterates over `PaymentForm.Meta.widgets` and asserts every widget's attrs includes `"class": "form-control"`. This is a static, fast test — no DB required.
- **FR-001 test**: Write an integration test `test_create_page_renders_col_md_6` that uses `django.test.Client` to GET the payment create page and asserts the response content contains `col-md-6` (not `col-12`). Django TestClient will render the template with form widget context, confirming the CSS class appears in the HTML.
- **Regression**: All existing tests must re-pass after changes.

### Edge cases

- **Disabled fields in edit mode**: When fields are disabled via `self.fields[field].disabled = True`, Django still renders the widget with the attrs defined in `Meta.widgets`, so `form-control` will be present on disabled inputs too — consistent with the standard.
- **File input styling**: Bootstrap 5 supports `form-control` on `<input type="file">` elements. The CSV upload form already uses this pattern successfully (`forms.FileInput(attrs={"class": "form-control"})`).
- **Mode variable**: The template uses a `mode` context variable to toggle between create and edit. This is preserved unchanged.
