# Quickstart: Payment Form Redesign

**Branch**: `023-redesign-payment-form`

## What needs to change

### 1. `backend/apps/payments/forms.py` — Add `form-control` to all widgets

Modify `PaymentForm.Meta.widgets` to include `"class": "form-control"` on every widget, and add widget entries for fields currently missing them:

```python
widgets = {
    "client": forms.Select(attrs={"class": "form-control"}),
    "amount": forms.NumberInput(attrs={"class": "form-control"}),
    "payment_type": forms.Select(attrs={"class": "form-control"}),
    "payment_identifier": forms.TextInput(attrs={"class": "form-control"}),
    "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    "class_slot_count": forms.NumberInput(attrs={"class": "form-control"}),
    "reference": forms.TextInput(attrs={"class": "form-control"}),
    "evidence": forms.FileInput(attrs={"class": "form-control"}),
    "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
}
```

### 2. `backend/apps/payments/templates/payments/payment_form.html` — Fix field columns

Change the field wrapper in the loop:

```diff
-<div class="col-12">
+<div class="col-md-6">
```

The button row `<div class="col-12">` stays as-is.

### 3. `backend/tests/test_payments.py` — Add TDD compliance tests

Add two test methods:

```python
def test_all_widgets_have_form_control(self):
    """FR-003: Every widget in Meta.widgets must have form-control class."""
    for field_name, widget in PaymentForm.Meta.widgets.items():
        assert "class" in widget.attrs, f"{field_name} widget missing 'class' attr"
        assert "form-control" in widget.attrs["class"], \
            f"{field_name} widget missing 'form-control'"

def test_create_page_renders_col_md_6(self, logged_client):
    """FR-001: Payment create page renders fields with col-md-6."""
    response = logged_client.get("/payments/create/")
    assert response.status_code == 200
    assert 'col-md-6' in response.content.decode()
    assert 'col-12' not in response.content.decode()  # verify no old class
```

## Verify

```bash
# Run the existing test suite to confirm zero regressions
cd backend && python -m pytest tests/test_payments.py -v
```
