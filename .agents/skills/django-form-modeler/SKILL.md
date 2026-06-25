---
name: django-form-modeler
description: >
  Apply this skill whenever a Django HTML form needs to be created, updated, redesigned,
  or reviewed. Triggers include: "create a form", "add a new form", "update the form design",
  "fix the form layout", "new Django template for a form", "edit form view", "form page",
  or any request to produce or modify a Django template that contains an HTML form element.
  Also triggers when reviewing or comparing existing form templates for consistency.
  Always apply this skill before generating any Django form HTML to ensure layout, field
  structure, Bootstrap 5 classes, CSRF handling, and nav chrome all follow the project spec.
---

# Django Form Modeler

This skill defines the canonical design spec for Django form pages in this project.
Apply it every time a form template is created or updated so all forms stay consistent.

The project uses **Bootstrap 5**, **HTMX**, **Django CSRF tokens**, and a shared dark navbar.

---

## Page Structure

Every form page follows this exact skeleton:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}</title>
  <link href="<path>/bootstrap.min.css" rel="stylesheet">
  <script src="<path>/htmx.min.js" integrity="sha384-..." crossorigin="anonymous"></script>
</head>
<body>
  <!-- 1. Navbar (always present) -->
  {% include "partials/navbar.html" %}   {# or inline; see Navbar spec below #}

  <!-- 2. Main content wrapper -->
  <main class="container-fluid">
    <!-- 3. Page heading -->
    <h2>{{ form_title }}</h2>

    <!-- 4. The form -->
    <form method="post" class="row g-3">
      {% csrf_token %}
      <!-- fields here -->
      <!-- action buttons here -->
    </form>
  </main>

  <!-- 5. JS at bottom -->
  <script src="<path>/chart.js@4"></script>
  <script src="<path>/bootstrap.bundle.min.js"></script>
  <script>/* HTMX CSRF handler — see HTMX section */</script>
</body>
</html>
```

Key rules:
- `lang="es"` on `<html>` (project language is Spanish).
- `<main class="container-fluid">` wraps all page content below the navbar.
- The `<h2>` page heading has no extra classes unless the form has a bottom-margin need (`class="mb-4"` is acceptable on edit pages).
- The `<form>` always uses `method="post"` and `class="row g-3"`.
- `{% csrf_token %}` is the first thing inside every `<form>`.

---

## Navbar

The navbar is shared across all pages. Inline it verbatim (or via `{% include %}`) with this structure:

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="{% url 'home' %}">Reserva de Cardio</a>
    <ul class="navbar-nav ms-auto">
      <li class="nav-item"><a class="nav-link" href="{% url 'reservations' %}">Reservaciones</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'clients_search' %}">Clientes</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'equipment' %}">Equipo</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'classes' %}">Horario</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'payments' %}">Pagos</a></li>
      <li class="nav-item"><a class="nav-link" href="{% url 'admin:index' %}">Admin</a></li>
      <li class="nav-item">
        <form method="post" action="{% url 'logout' %}" class="d-inline">
          {% csrf_token %}
          <button type="submit" class="nav-link btn btn-link">Cerrar sesión</button>
        </form>
      </li>
    </ul>
  </div>
</nav>
```

Notes:
- `navbar-dark bg-dark mb-4` — dark background, white links, bottom margin before content.
- Nav links are right-aligned via `ms-auto` on the `<ul>`.
- Logout is a POST `<form>` with its own `{% csrf_token %}`, inline via `d-inline`.
- No hamburger toggler is currently used; add one only if explicitly requested.

---

## Form Field Layout

Fields are laid out in a **Bootstrap 5 grid** using column classes inside the `row g-3` form.

### Column widths

| Field type              | Class          |
|-------------------------|----------------|
| Short text / select     | `col-md-6`     |
| Email / phone           | `col-md-6`     |
| Textarea / long text    | `col-md-6`     |
| Action buttons          | `col-12`       |

Use `col-md-6` for most fields so two fields appear side-by-side on medium+ screens.
Use `col-12` only for the button row or a field that must span the full width.

### Field wrapper

```html
<div class="col-md-6">
  <label class="form-label">Field Label</label>
  <input type="text" name="field_name" class="form-control" ... >
</div>
```

- `<label>` always has `class="form-label"`. No `for` attribute is required unless accessibility is explicitly requested (Django renders `id_<field>` automatically).
- Every input/select/textarea gets `class="form-control"`.
- Validation attributes (`required`, `maxlength`, `type`) are added as appropriate.
- Do NOT wrap fields in extra `<div>` layers beyond the column wrapper.

### Input types by field

| Django field type   | HTML element                                   |
|---------------------|------------------------------------------------|
| CharField           | `<input type="text">`                          |
| EmailField          | `<input type="email">`                         |
| ChoiceField / FK    | `<select>` with `<option>` list                |
| TextField           | `<textarea cols="40" rows="3">`                |
| BooleanField        | `<input type="checkbox">` (unstyled or switch) |

For `<select>`, always include an empty first option:
```html
<option value="">---------</option>
```

---

## Action Buttons

The button row is always `col-12` and placed **last** inside the form:

```html
<div class="col-12">
  <button type="submit" class="btn btn-primary">Guardar</button>
  <a href="{% url 'cancel_target' %}" class="btn btn-secondary">Cancelar</a>
</div>
```

Rules:
- Submit button: `btn btn-primary`, label "Guardar".
- Cancel link: `btn btn-secondary`, label "Cancelar", href points to the list page for that resource.
- No other button styles unless explicitly specified.
- Buttons are not wrapped in additional divs.

---

## HTMX CSRF Handler

Include this `<script>` block at the bottom of every page that uses HTMX:

```html
<script>
  document.body.addEventListener('htmx:configRequest', function(evt) {
    var cookies = document.cookie.split('; ');
    var csrfToken = null;
    for (var i = 0; i < cookies.length; i++) {
      var parts = cookies[i].split('=');
      if (parts[0] === 'csrftoken') {
        csrfToken = decodeURIComponent(parts.slice(1).join('='));
        break;
      }
    }
    if (csrfToken) {
      evt.detail.headers['X-CSRFToken'] = csrfToken;
    }
  });
</script>
```

This injects the CSRF token into every HTMX-initiated request automatically.

---

## Language

All visible user-facing text is in **Spanish**:

| English            | Spanish              |
|--------------------|----------------------|
| First name         | Nombre               |
| Last name          | Apellido             |
| Email              | Correo electrónico   |
| Mobile / Phone     | Móvil                |
| Equipment name     | Nombre               |
| Equipment type     | Tipo de equipo       |
| Status             | Estado               |
| Notes              | Notas                |
| Save               | Guardar              |
| Cancel             | Cancelar             |
| Log out            | Cerrar sesión        |
| Reservations       | Reservaciones        |
| Clients            | Clientes             |
| Equipment          | Equipo               |
| Schedule           | Horario              |
| Payments           | Pagos                |

Extend this table as new fields/labels are added. Always match existing Spanish labels for recurring concepts.

---

## Select Option Values (Equipment)

When generating the equipment type select, use these exact values and labels:

```html
<option value="">---------</option>
<option value="climber">Escaladora</option>
<option value="treadmill">Cinta de correr</option>
<option value="bike">Bicicleta estacionaria</option>
<option value="elliptical">Elíptica</option>
<option value="rower">Máquina de remo</option>
<option value="other">Otro</option>
```

Status select:
```html
<option value="in-service">En servicio</option>
<option value="out-of-service">Fuera de servicio</option>
```

---

## Checklist Before Generating a Form

Before writing any form template, verify:

- [ ] `<html lang="es">` present
- [ ] Bootstrap 5 CSS linked in `<head>`
- [ ] HTMX script in `<head>`
- [ ] Navbar included with all nav links and logout form
- [ ] `<main class="container-fluid">` wrapping content
- [ ] `<h2>` heading with form name
- [ ] `<form method="post" class="row g-3">`
- [ ] `{% csrf_token %}` as first child of form
- [ ] Each field in `<div class="col-md-6">` with `form-label` + `form-control`
- [ ] Button row in `<div class="col-12">` with `btn-primary` submit and `btn-secondary` cancel
- [ ] `chart.js@4` and `bootstrap.bundle.min.js` at bottom
- [ ] HTMX CSRF handler script at bottom
- [ ] All labels and options in Spanish

---

## Reference: Canonical Examples

See `references/examples.md` for the two reference forms (new_client and edit_equipment) with annotations explaining each design decision.
