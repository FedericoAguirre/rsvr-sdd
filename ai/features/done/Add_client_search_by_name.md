# Add client search by name

## Description

- As an Operator I want to be able to search a Client by name.
- Keeping the actual search options by email or mobile number.
- I want to use at least 3 letters, to start the search.
- The search must be case insensitive.

## Inputs

- The clients/search/ endpoint
- The textbox with id="id_q"

## Outputs

- The Client or Clients that meet the search condition.

## Acceptance criteria

- If any Client meets the search condition must be shown in the list.
- The filter must be colored in the Client names.
- If no Client is found, there must be an alert indicating: "Client NOT FOUND". Make use of HTMX, if necessary.
- If HTMX is used, add it as part of the system architecture and modify the proper documents to use it for interactivity.