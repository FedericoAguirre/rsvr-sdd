# Quickstart: Batch Reservation Weekly Date Groups

## Prerequisites

- Running Django development server: `cd backend && uv run manage.py runserver`
- A payment with `class_slot_count > 0` (so the batch modal triggers)
- Test fixtures: `cd backend && uv run manage.py dumpdata payments.Payment --pk=1`

## Validation Scenarios

### Scenario 1: Weekly Grid Layout

**Steps**:
1. Open a payment detail page that triggers the batch modal (e.g., after creating a payment via `/payments/create/`)
2. Or manually navigate to `/payments/{id}/?batch_modal=1` where `id` has a payment with `class_slot_count > 0`

**Expected**:
- The modal opens with a 5-column grid showing available dates
- Column headers read: Lun | Mar | Mié | Jue | Vie
- Dates are organized in 4 rows (one per week)
- Each week group has visual separation (light `<hr>` or spacing)
- Each button shows date in format `DD/M` (e.g., "15/1")

**Pass/Fail**: All 4 rows × 5 columns visible with day headers and date buttons in correct columns.

---

### Scenario 2: Date Selection

**Steps**:
1. Click a date button — it should turn blue (`.btn-primary`)
2. Click the same button again — it should return to outline style (`.btn-outline-secondary`)
3. Select 3 dates — the selection count (`#dateCount`) should display "3"

**Expected**:
- Click toggles active state correctly
- Count updates in real-time
- "Create Reservations" button is disabled when 0 dates selected, enabled when selection matches `block_class_count`

**Pass/Fail**: Selection behavior matches existing modal behavior.

---

### Scenario 3: Form Submission

**Steps**:
1. Select the required number of dates (equal to `block_class_count`)
2. Click "Create Reservations"

**Expected**:
- The page redirects to the payment detail page
- The new reservations appear in the "Associated Reservations" table
- No errors are shown

**Pass/Fail**: Batch reservation creation works correctly with the new grid layout.

---

### Scenario 4: Responsive Behavior

**Steps**:
1. Open the modal on a 1920×1080 desktop — verify no vertical scroll needed
2. Resize browser to 768px width — verify 5-column grid is preserved
3. Resize browser to 375px width — verify dates are readable, no horizontal overflow

**Expected**:
- 5-column layout preserved across all breakpoints
- `.modal-dialog-scrollable` handles any vertical overflow gracefully
- No horizontal scrollbar appears

**Pass/Fail**: Grid is usable at all viewport widths without horizontal overflow.

---

### Scenario 5: Existing Tests

**Steps**:
```bash
cd backend && uv run pytest tests/test_payments_batch.py -v --tb=short
```

**Expected**: All existing batch tests pass (backend changes only — visual changes don't affect backend tests).

**Pass/Fail**: All tests green.

---

### Scenario 6: i18n — Day Labels

**Steps**:
1. Check Spanish translation file: `grep -n "Lun\|Mar\|Mié\|Jue\|Vie\|Sáb\|Dom" backend/locale/es/LC_MESSAGES/django.po`
2. Check that `payment_detail.html` references day labels via `{% translate %}` or `{% blocktrans %}`

**Expected**: All 7 day abbreviations are registered in `django.po` with Spanish translations. No hardcoded day strings in the template.

**Pass/Fail**: i18n scans pass with no hardcoded user-visible strings.

---

## Details

- **Contracts**: See [contracts/README.md](contracts/README.md) for UI invariants
- **Data Model**: See [data-model.md](data-model.md) for client-side date structures
- **Spec**: See [spec.md](spec.md) for functional requirements
