# 3. Create a Button to access to reservations_payments webpage

As an system Operator I want to access to the <payment_id>/associate/ webpage, using an **Associate button** included
in the payments/{payment_id}/ webpage.

The **Associate** button must be placed at the left of the **Edit** button.

The tabs order in the form must be reordered accordingly.

## Acceptance criteria

- The **Associate** button is placed at the left of the **Edit** button.
- the tabs order is reordered.
- When the **Associate** button is pushed, I can associate the current payment using the payments/{payment_id}/ webpage functionality.

## Implementation Notes (2026-07-02)

- Added `Associate` button to `payment_detail.html` card header, positioned left of `Edit`
- Added `get()` method to `PaymentAssociateView` (POST-only before) to render available reservations
- Created new template `payment_associate.html` with reservation selection table
- Added i18n key `Associate` → `Asociar` in `backend/locale/es/LC_MESSAGES/django.po`
- Tab order determined by DOM source order (project convention)
- Button styled `btn-outline-info` per research decision
- 5 tests written and passing (TDD)
