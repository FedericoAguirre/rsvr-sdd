# CSV Client upload

## Description

As a system operator, I want to upload or update client data using a CSV file.

## Specifications

The CSV file will have these columns:

- first_name (required)
- last_name (required)
- email (optional)
- mobile (optional)

Although email and mobile are marked as optional, the CSV file must have one, the other or both.

The CSV file will have a header, with the previous columns and order.

For each record in the file:

- Verify if the first_name and last_name matches (no matter the letter case) with an existing user, update email and or mobile if needed.
- If the email or mobile are found, check if the other fields need to be updated and update them.

Do a basic data cleansing before processing the file.

Provide feedback to the user, telling stats for records in file, new and updated users, after processing.

The new records MUST BE set to ACTIVE,

The client's creation and update dates must be handled accordingly.
