# Canonical Form Examples

These two forms are the reference implementation for the project's form design spec.
Study them when in doubt about any structural or visual decision.

---

## Example 1: New Client Form (`new_client.html`)

**Purpose:** Create a new client record.
**Fields:** Nombre (text), Apellido (text), Correo electrónico (email), Móvil (text)
**Cancel target:** `/clients/search/`

### Annotated structure

```html
<h2>Nuevo Cliente</h2>                         <!-- no mb-4 on creation forms -->
<form method="post" class="row g-3">
    {% csrf_token %}

    <div class="col-md-6">                     <!-- half-width column -->
        <label class="form-label">Nombre</label>
        <input type="text" name="first_name" class="form-control"
               maxlength="100" required id="id_first_name">
    </div>

    <div class="col-md-6">
        <label class="form-label">Apellido</label>
        <input type="text" name="last_name" class="form-control"
               maxlength="100" required id="id_last_name">
    </div>

    <div class="col-md-6">
        <label class="form-label">Correo electrónico</label>
        <input type="email" name="email" class="form-control"
               maxlength="254" id="id_email">   <!-- not required -->
    </div>

    <div class="col-md-6">
        <label class="form-label">Móvil</label>
        <input type="text" name="mobile" class="form-control"
               maxlength="20" id="id_mobile">   <!-- not required -->
    </div>

    <div class="col-12">                       <!-- full-width button row -->
        <button type="submit" class="btn btn-primary">Guardar</button>
        <a href="/clients/search/" class="btn btn-secondary">Cancelar</a>
    </div>
</form>
```

**Design notes:**
- Four fields in two rows, each `col-md-6` (side-by-side on md+).
- `first_name` and `last_name` are `required`; email and mobile are optional.
- `<h2>` has no additional classes on a "new" form page.

---

## Example 2: Edit Equipment Form (`edit_equipment.html`)

**Purpose:** Edit an existing equipment record (pre-populated values).
**Fields:** Nombre (text), Tipo de equipo (select), Estado (select), Notas (textarea)
**Cancel target:** `/equipment/`

### Annotated structure

```html
<h2 class="mb-4">Editar Equipo</h2>           <!-- mb-4 present on edit forms -->
<form method="post" class="row g-3">
    {% csrf_token %}

    <div class="col-md-6">
        <label class="form-label">Nombre</label>
        <input type="text" name="name" value="{{ equipment.name }}"
               class="form-control" maxlength="100" required id="id_name">
    </div>

    <div class="col-md-6">
        <label class="form-label">Tipo de equipo</label>
        <select name="equipment_type" class="form-control" required id="id_equipment_type">
            <option value="">---------</option>
            <option value="climber" {% if equipment.equipment_type == "climber" %}selected{% endif %}>Escaladora</option>
            <option value="treadmill" {% if equipment.equipment_type == "treadmill" %}selected{% endif %}>Cinta de correr</option>
            <option value="bike" {% if equipment.equipment_type == "bike" %}selected{% endif %}>Bicicleta estacionaria</option>
            <option value="elliptical" {% if equipment.equipment_type == "elliptical" %}selected{% endif %}>Elíptica</option>
            <option value="rower" {% if equipment.equipment_type == "rower" %}selected{% endif %}>Máquina de remo</option>
            <option value="other" {% if equipment.equipment_type == "other" %}selected{% endif %}>Otro</option>
        </select>
    </div>

    <div class="col-md-6">
        <label class="form-label">Estado</label>
        <select name="status" class="form-control" id="id_status">
            <option value="in-service" {% if equipment.status == "in-service" %}selected{% endif %}>En servicio</option>
            <option value="out-of-service" {% if equipment.status == "out-of-service" %}selected{% endif %}>Fuera de servicio</option>
        </select>
    </div>

    <div class="col-md-6">
        <label class="form-label">Notas</label>
        <textarea name="notes" cols="40" rows="3"
                  class="form-control" id="id_notes">{{ equipment.notes }}</textarea>
    </div>

    <div class="col-12">
        <button type="submit" class="btn btn-primary">Guardar</button>
        <a href="/equipment/" class="btn btn-secondary">Cancelar</a>
    </div>
</form>
```

**Design notes:**
- Edit form heading uses `mb-4` (spacing before a form with pre-filled data).
- `<textarea>` uses `cols="40" rows="3"` — do not change default dimensions.
- `<select>` for status has no empty `--------` option (status is always known).
- Equipment type select does include the empty option as a fallback/reset choice.
- Textarea and selects are still `col-md-6`, same as text inputs.

---

## Pattern Summary

| Scenario            | `<h2>` classes | Notes field | Required fields         |
|---------------------|----------------|-------------|-------------------------|
| New record form     | _(none)_       | Optional    | Core identity fields    |
| Edit record form    | `mb-4`         | Optional    | Name/type always required |

When in doubt, match the closest existing example from this file.
