# Add client list

## Description

In the clients/search/ endpoint, I want to add the Clients list.

The list must show all the Client attributes.

If the Clients list is bigger than 10, implement pagination.

Each Client row must have a link or button to Edit that Client.

The list must be shown, when the Operator enters to the clients/search/ 

The clients/search/ endpoint has a Client counter widget.

## Inputs

- The Client model.
- The clients/search/ endpoint

## Outputs

- The Clients list is shown in the clients/search/ endpoint.

## Acceptance criteria

- The Clients list is shown in the clients/search/ endpoint.
- The Clients list is paginated and tested with at least 21 clients.
- Each Client record can be modified from here.
- The client counter widget is shown in the clients/search/ endpoint.
## Additional Requests (added during implementation)

- Change counter label to "X Clientes" (Spanish)
- Add seed migration with 5 fake clients (Lucía García, Carlos López, María Rodríguez, Pedro Martínez, Ana Fernández)
- Sort client list by last name, then first name
