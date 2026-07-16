# Session: Order Reservations by Date on Payment Detail

**Branch**: `042-order-reservations-date`
**Model**: deepseek-v4-flash

## Work Done

- Root cause identified: `PaymentDetailView.get_context_data()` had no `.order_by()` on `payment_reservations` queryset
- Fix: Added `.order_by("-reservation__date", "-reservation__class_slot__time")` at `views.py:130`
- Pattern already used in `PaymentAssociateView` — consistent approach

## Tests Added

3 new TDD tests in `test_payments.py` — all passing:
- Date descending order
- Same-date sorted by class slot time descending
- Empty list regression (no crash)

Plus 2 fixtures: `class_slot_early`, `class_slot_late`

## Total Test Count

**220 passed, 8 pre-existing failures** (unrelated to this feature)

## Files Changed

- `backend/apps/payments/views.py:130` — added `.order_by("-reservation__date", "-reservation__class_slot__time")`
- `backend/tests/test_payments.py` — 3 ordering tests + 2 fixtures
- `.specify/feature.json` — updated
- `AGENTS.md` — updated to point to plan

## Spec Artifacts

`specs/042-order-reservations-date/` — spec.md, plan.md, tasks.md, research.md, data-model.md, quickstart.md, checklists/ (all complete)
