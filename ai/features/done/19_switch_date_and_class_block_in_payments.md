# Switch date and class block columns in payments, add stripe to grid

## User story

As an app operator, I want to switch the column order of the "Reservas asociadas" grid on the `payments/{id}/` page to Bloque de clase, Fecha, Equipo, Estado and add striped rows, so that I can identify the class block and date more easily at a glance.

## Acceptance criteria

Given I am viewing the "Reservas asociadas" section on the `payments/{id}/` page,
When the reservation list loads,
Then the columns appear in the order: Bloque de clase, Fecha, Equipo, Estado.

Given I navigate between different payment detail pages,
When each page loads,
Then the column order remains Bloque de clase, Fecha, Equipo, Estado consistently.

Given the page is refreshed or reloaded,
When the reservation history renders,
Then the grid has alternating row background colors (striped) for better readability.

## Definition of Done

- The column order in the "Reservas asociadas" table on `payments/{id}/` is changed to: Bloque de clase, Fecha, Equipo, Estado
- The `<table>` element has the Bootstrap `table-striped` class applied
- The change applies to all interactions (initial load, navigation, refresh)
- No other columns or data are affected
- Existing functionality (links, status display) remains unchanged
