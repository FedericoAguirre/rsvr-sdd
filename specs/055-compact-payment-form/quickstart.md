# Quickstart: Compact Payment Form Layout

## Prerequisites

- PostgreSQL running (`make db-up`)
- Django migrations up to date (`uv run manage.py migrate`)
- Dev server running (`uv run manage.py runserver`)

## Validation Scenarios

### 1. Desktop Single-Screen Fit

1. Open `http://localhost:8000/payments/create/` on a 1920×1080 display
2. Verify no vertical scrollbar is visible (all fields and buttons on screen)
3. Verify the title is rendered as `h4` (smaller than before)
4. Verify the form width is contained (max ~900px centered)

**Expected**: Form fits entirely in viewport without scrolling.

### 2. Help Text Interaction

1. Tab into any form field
2. Verify help text appears below the focused field
3. Tab away from the field (leaving it empty)
4. Verify help text disappears
5. Enter a value and tab away
6. Verify help text stays hidden (or shows on re-focus)

**Expected**: Help text toggles on focus/blur as described.

### 3. Multi-Column Layouts

1. Inspect the Documentation and Reference fieldset
2. Verify payment_identifier, reference, and evidence are in a single row (3 × `col-md-4`)
3. Inspect the Context fieldset
4. Verify date and notes are side-by-side (2 × `col-md-6`)
5. Inspect Transaction Data fieldset
6. Verify amount and class_slot_count are side-by-side (2 × `col-md-6`)

**Expected**: Three distinct column patterns visible.

### 4. Responsive Breakpoints

1. Resize browser to 768px width
2. Verify all multi-column layouts stack to full-width
3. Verify buttons stack vertically
4. Resize to 375px width
5. Verify no horizontal overflow

**Expected**: Form degrades gracefully at each breakpoint.

### 5. Form Submission

1. Fill all required fields
2. Click "Crear pago"
3. Verify payment is created (redirect to detail page)

**Expected**: Form submission works identically to before.

### 6. Edit Mode

1. Navigate to an existing payment's edit page
2. Verify compact layout applies (all fields visible without scrolling)
3. Save changes
4. Verify update is successful

**Expected**: Edit mode also uses compact layout.

## Test Commands

```bash
# Run payment-related tests
cd backend && uv run pytest apps/payments/tests/ -v

# Run all tests
cd backend && uv run pytest -v
```

## Key Files

- **Template**: `backend/apps/payments/templates/payments/payment_form.html`
- **Form class**: `backend/apps/payments/forms.py` (no changes expected)
- **Spec**: `specs/055-compact-payment-form/spec.md`
- **Data model**: `specs/055-compact-payment-form/data-model.md`
