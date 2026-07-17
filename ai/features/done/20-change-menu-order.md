# Change the menu order

## User story

As a system operator, I want to change the navigation bar menu order so that I can improve my workflow.

The menu order, from left to right, should be:

1. Clientes
2. Pagos
3. Reservaciones
4. Equipo
5. Horario
6. Reportes
7. Admin
8. Cerrar Sesión

## Acceptance criteria

Given I navigate to any page in the application,
When the navigation bar renders,
Then the menu items appear in the order: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión.

Given I click on any menu item,
When the page loads,
Then the new page shows the navigation bar with the same menu order preserved.

Given I am on a mobile or narrow viewport,
When the navigation bar collapses,
Then the menu items appear in the specified order in the hamburger menu.

## Definition of Done

- The navigation bar menu items are reordered to: Clientes, Pagos, Reservaciones, Equipo, Horario, Reportes, Admin, Cerrar Sesión
- The order is consistent across all web pages
- No functionality is affected (all links, dropdowns, and active states work as before)
- The change applies to all viewport sizes (responsive)
