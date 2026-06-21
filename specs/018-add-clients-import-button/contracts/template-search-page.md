# Template Contract: Clients Search Page

**File**: `backend/apps/clients/templates/clients/search.html`

**Route**: `GET /clients/search/` (name: `clients:client-search`)

## Current Elements

| Element | Implementation | i18n Key | Notes |
|---------|---------------|----------|-------|
| Page title | `<h2>{% translate "Search Clients" %}</h2>` | `Search Clients` → `Buscar Clientes` | |
| Search input | `{{ form.q }}` with placeholder `_("Search clients...")` | `Search clients...` → `Buscar clientes...` | HTMX live search |
| Search button | `<button>{% translate "Search" %}</button>` | `Search` → `Buscar` | |
| New Client link | `<a href="{% url 'clients:client-create' %}">{% translate "New Client" %}</a>` | `New Client` → `Nuevo Cliente` | Bootstrap `btn btn-success` |
| Search indicator | `<span>{% translate "Searching..." %}</span>` | `Searching...` → `Buscando...` | HTMX indicator |

## Required Changes

### 1. Add "Subir Clientes" Navigation Element

Add a link alongside the existing action buttons in the `<form>` row:

```html
<a href="{% url 'clients:client-csv-upload' %}" class="btn btn-info">{% translate "Upload Clients" %}</a>
```

- **Element type**: `<a>` (link) styled as Bootstrap button
- **CSS class**: `btn btn-info` (distinct from "New Client" green `btn-success`)
- **Route**: `clients:client-csv-upload` (existing, points to `/clients/upload/`)
- **i18n**: Must use `{% translate "Upload Clients" %}`

### 2. Add i18n Entry

In `backend/locale/es/LC_MESSAGES/django.po`, add:

```
msgid "Upload Clients"
msgstr "Subir Clientes"
```

Then recompile: `django-admin compilemessages`

### 3. No Changes to URLs or Views

- `backend/apps/clients/urls.py` — unchanged (upload route already registered)
- `backend/apps/clients/views.py` — unchanged

## Test Verification

| Assertion | Test Type | Method |
|-----------|-----------|--------|
| "Subir Clientes" link present on search page | Integration | `assertContains(response, "Subir Clientes")` |
| Link points to `/clients/upload/` | Integration | `assertContains(response, "/clients/upload/")` |
| Spanish label renders correctly | i18n | `assertContains(response, "Subir Clientes")` with Spanish locale |
| Click navigates correctly | Integration | `response = client.get("/clients/upload/")` |
