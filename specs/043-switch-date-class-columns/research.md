# Research: Switch Date and Class Block Columns in Payments History

## Overview

Investigate the current reservation history table structure on the client detail page to confirm the exact file, column order, and any potential side effects.

## Finding: Template Location

- **File**: `backend/apps/clients/templates/clients/client_detail.html`
- **Table lines**: 35–49
- **Current column order in HTML**: `Date` (`Fecha`), `Class` (`Clase`), `Equipment` (`Equipo`)

## Finding: Current Order

```html
<thead>
  <tr>
    <th>{% translate "Date" %}</th>      <!-- renders as "Fecha" -->
    <th>{% translate "Class" %}</th>     <!-- renders as "Clase" -->
    <th>{% translate "Equipment" %}</th> <!-- renders as "Equipo" -->
  </tr>
</thead>
<tbody>
  {% for r in reservations %}
  <tr>
    <td>{{ r.date }}</td>
    <td>{{ r.class_slot }}</td>
    <td>{{ r.equipment }}</td>
  </tr>
  {% endfor %}
</tbody>
```

## Finding: Desired Order

```html
<thead>
  <tr>
    <th>{% translate "Class" %}</th>     <!-- Clase -->
    <th>{% translate "Date" %}</th>      <!-- Fecha -->
    <th>{% translate "Equipment" %}</th> <!-- Equipo -->
  </tr>
</thead>
<tbody>
  {% for r in reservations %}
  <tr>
    <td>{{ r.class_slot }}</td>
    <td>{{ r.date }}</td>
    <td>{{ r.equipment }}</td>
  </tr>
  {% endfor %}
</tbody>
```

## Finding: i18n Status

All three column labels are already translated in `backend/locale/es/LC_MESSAGES/django.po`. No new translation keys needed.

## Finding: No View Changes Required

The template receives `reservations` queryset from `client_detail` view. Column order is purely a template concern — no backend changes needed.

## Decision

- **Approach**: Reorder `<th>` and `<td>` elements in `client_detail.html`
- **Files to modify**: 1 (template)
- **New test files**: 1 (`test_client_detail.py`)
- **No CSS, JS, or backend changes required**
- **No i18n changes required**
