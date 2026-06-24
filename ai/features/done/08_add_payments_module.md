# Payments module

## Description

As a system user, I want to be able to register payments for the classes.
Today, all payments are made by hand and saved in a spreadsheet.
The first step is to save them within the system.
In the future, we intend to enable the clients to make payments online by themselves.

## Business rules

The business can receive payments in:

- Cash
- Credit card
- Debit card
- Electronic transfer
- Payments app
- Payments broker (in the future)
- Online (in the future)

The payments made by a client must have the following attributes:

- Date
- Client id
- Payment type
- Payment identifier
- Amount
- Class slot count
- Reference (optional)
- Evidence (image, optional)
- Notes (optional)
- Created at
- Created by (operator)
- Updated at
- Updated by (operator)

Note: The payment identifier can be a string made up of the payment type (2- or 3-letter acronym), date (YYYYMMDD), the client initials, and the 3-digit consecutive number for that day.

A Client's payment can be associated with the clients reservations by the number of Class slot count.

## UI

The payments module must be accessible from the Main menu like other modules.

A new payment can be created from the New Reservations webpage. The payment must exist before it can be associated to the Reservations.

An operator can see the payment history per client in a paginated way, each page is made up of 5 payments. The payments must be ordered by descending date.

Administrators need to see the payments summarized by day, week, month, or range of dates and grouped by payment type. The reports can have basic supporting graphics. The reports must aggregate amount, reservations per client, payment count, and any other derived metric.

## Reservations and payments integration

A Client payment can be related to N reservations, where N is the Class slot count in the Payment object.

An operator must be able to associate the Client payment and the Reservations.
