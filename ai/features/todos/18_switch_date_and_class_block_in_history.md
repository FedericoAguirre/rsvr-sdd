# Switch date and class block columns in the payments history

## User story

As an app operator, I want to switch the date and class block column order in the payment history on the client detail page, so that I can identify the day of class and the date more easily at a glance.

## Acceptance criteria

Given I am viewing the "Historial de Reservas" section on the `clients/{id}/` page,
When the reservation list loads,
Then the columns appear in the order: Clase, Fecha, Equipo.

Given I navigate between different client detail pages,
When each page loads,
Then the column order remains Clase, Fecha, Equipo consistently.

Given the page is refreshed or reloaded,
When the reservation history renders,
Then the column order is still Clase, Fecha, Equipo (persistent across requests).

## Definition of Done

- The column order in the reservation history table on `clients/{id}/` is changed to: Clase, Fecha, Equipo
- The change applies to all interactions (initial load, navigation, refresh)
- No other columns or data are affected
- Existing functionality (sorting, filtering, links) remains unchanged
