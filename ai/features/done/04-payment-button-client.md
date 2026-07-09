# 4. Add payment button to the clients/{client_id}/ webpage

As a system user I want to be able to add a new client's payment from the
clients/{client_id}/ webpage.

The page must have a **New Payment** button that redirects to the payments/create/
web page and preselects the Client combo box, using the current client_id.

The **New Payment" button must be placed at the right of the **Nueva Reserva**
button.

The payments/create/ can be accessed directly or by clicking the
clients/{client_id} **New Payment** button.

## Acceptance criteria

- The clients/{client_id} webpage has a **New Payment** button located at the
    right of the **Nueva Reserva** button.
- The payments/create/ webpage can create a new payment with an empty client (by direct access) or
    with a preselected one (by clicking the **New Payment** button at the
    clients/{client_id} webpage).
- As a system user when I click the **New Payment** button in the
    client/{client_id} I can create a new payment with the preselected client.
- The new text assets as displayed in Spanish, using the i18n assets.
