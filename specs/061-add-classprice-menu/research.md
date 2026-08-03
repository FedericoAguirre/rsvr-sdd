# Research: Add ClassPrice Sub-Option Under "Horario" Menu

## Research Questions

### R1: What is the existing dropdown pattern for the nav menu?

**Decision**: Replicate the "Reportes" dropdown pattern from `base.html` lines 31-36. The pattern uses Bootstrap 5.3's `nav-item dropdown` → `nav-link dropdown-toggle` → `dropdown-menu` → `dropdown-item` structure with `data-bs-toggle="dropdown"`.

**Rationale**: The existing "Reportes" dropdown (lines 31-36) is already styled and functional. Replicating its exact HTML structure and CSS classes ensures visual consistency and proper Bootstrap behavior on both desktop and mobile.

**Source**: `backend/templates/base.html` lines 31-36:
```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">{% translate "Reports" %}</a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{% url 'payments:reports' %}">{% translate "Payments" %}</a></li>
    </ul>
</li>
```

### R2: Does the "Reportes" dropdown work on mobile?

**Decision**: Yes. Bootstrap's `navbar-expand-lg` + `collapse navbar-collapse` handles the responsive behavior. The dropdown works inside the collapsible nav on mobile (`< 992px`) and expands as a horizontal bar on desktop.

**Rationale**: The nav uses Bootstrap's standard responsive navbar pattern. No additional mobile-specific handling is needed.

### R3: What translations are needed for the new dropdown?

**Decision**: All required translations already exist in `django.po`:
- `"Schedule"` → `"Horario"` (line 1312) — dropdown toggle label
- `"Class Schedule"` → `"Horario de Clases"` (line 206-207) — first dropdown item
- `"Class prices"` → `"Precios de clase"` (line 131) — second dropdown item

**Rationale**: These msgids are already internationalized. The `{% translate %}` tag will resolve them from the existing `.po` file. No new translations needed.

### R4: Does `classes:price-list` URL work without a `class_slot` parameter?

**Decision**: Yes. After spec 059, `ClassPricesView` lists all prices globally (no class_slot context required). The URL `classes:price-list` maps to `/classes/prices/` with no path parameters.

**Rationale**: Verified in `urls.py` line 9: `path("prices/", views.ClassPricesView.as_view(), name="price-list")`. No kwargs needed.

### R5: Should both dropdown items share the same permission gate?

**Decision**: Yes. Both the schedule and the price list are gated behind `perms.classes.view_classslot`. The entire dropdown is wrapped in `{% if perms.classes.view_classslot %}`.

**Rationale**: Spec assumption states both links share the same permission. No separate permission for ClassPrice view exists, and creating one would expand scope beyond the spec.

## Summary

Template-only change: replace the flat `<a>` link at `base.html` line 28 with a dropdown following the "Reportes" pattern (lines 31-36). Two existing URLs, existing i18n translations, existing permissions. No new code, no migrations, no tests needed beyond the existing test suite.
