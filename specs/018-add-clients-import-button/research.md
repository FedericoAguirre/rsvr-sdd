# Research: Add Clients Import Button

## Overview

This document consolidates research findings for adding a "Subir Clientes" navigation element on the clients search page.

## Unknowns Resolved

### 1. What does "Búsqueda..." refer to in the clients/search/ page?

- **Finding**: The search page (`search.html`) renders a form with a text input (`{{ form.q }}`). The placeholder attribute is set to `_("Search clients...")` which translates to "Buscar clientes..." (not "Búsqueda...") in the compiled `.po` file. The user's description uses "Búsqueda..." as a colloquial reference to the search-related label/legend on the page.
- **Decision**: Replace the search input's placeholder text with a "Subir Clientes" link/button adjacent to or replacing the search input area. The exact positioning will be to replace the placeholder text display element, not the functional search input itself — the search functionality must be preserved.

### 2. Where should the "Subir Clientes" element be placed?

- **Finding**: The search page currently has a search input, a "Search" button, and a "New Client" button in a horizontal row. The most natural position is alongside the existing action buttons, replacing or adjacent to the search label area.
- **Decision**: Place the "Subir Clientes" link after the search input and Search button, alongside the existing "New Client" button. This maintains the existing layout pattern and provides clear visual access.

### 3. Button or link?

- **Finding**: The action is navigation to another page (`/clients/upload/`), not an in-page action. Per web standards, a link (`<a>`) is semantically correct for navigation. Django's `{% url %}` tag and Bootstrap's `btn` classes can style it identically to a button.
- **Decision**: Use an `<a>` tag styled as a Bootstrap button (`btn btn-primary` or similar). This provides the visual affordance of a button with the correct semantic behavior of a link.

### 4. What about the "Búsqueda..." placeholder after replacement?

- **Finding**: The search input must remain functional — users still need to search clients. The placeholder text can be updated to something shorter or more generic.
- **Decision**: Keep the search input with a simplified placeholder. The "Subir Clientes" element is placed adjacent in the UI, not replacing the input itself.

### 5. Are there existing patterns for navigation elements on the search page?

- **Finding**: The search page already has:
  - Search input (`{{ form.q }}`) with placeholder
  - "Search" submit button
  - "New Client" link (`btn btn-success`) that navigates to `/clients/create/`
  - HTMX-powered live search with indicator
- **Decision**: Follow the existing "New Client" link pattern for the "Subir Clientes" element — an `<a>` tag with Bootstrap button classes and `{% url 'clients:client-csv-upload' %}` as href.

### 6. i18n requirements

- **Finding**: The constitution requires all user-facing text to use Django i18n. The `locale/es/LC_MESSAGES/django.po` file contains all existing translations.
- **Decision**: Add `{% translate "Upload Clients" %}` in the template and add the corresponding `msgid "Upload Clients"` / `msgstr "Subir Clientes"` entry in `django.po`, then recompile with `django-admin compilemessages`.

## Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Element type | `<a>` link styled as Bootstrap button | Navigation action; follows existing "New Client" pattern |
| Placement | Alongside existing action buttons in the form row | Preserves layout, follows existing UX pattern |
| i18n approach | `{% translate %}` + `django.po` entry | Constitution mandate, existing project convention |
| Test approach | pytest-django integration test | Existing test patterns; verifies rendered HTML contains expected element |

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| `<button>` element | Semantically incorrect for navigation; requires JS for `window.location` |
| Replace search input entirely | Breaks core search functionality |
| Separate row for the link | Adds unnecessary vertical space; existing horizontal layout sufficient |
