# Research: Reorder Payment Form Fields

## 1. Django ModelForm Field Ordering

**Decision**: Reorder fields by changing the `fields` list in `Meta.fields` on the existing `PaymentForm`.

**Rationale**: Django renders ModelForm fields in the order defined in `Meta.fields`. Reordering the list is the simplest and most maintainable approach. An alternative (`field_order` attribute on the form) also works but adds an extra mechanism when the fields list itself can be reordered.

**Alternatives considered**:
- Using `field_order` form attribute — functionally equivalent but adds an additional attribute to maintain alongside `Meta.fields`.
- Reordering in the template only — would introduce a mismatch between form field order and visual order, making future maintenance confusing.
- Template-only layout with explicit field rendering — the current template likely uses `{{ form.as_p }}` or similar; switching to explicit field rendering gives full control over layout and responsive design.

## 2. Bootstrap 5 Form Layout

**Decision**: Render fields explicitly in the template with Bootstrap 5 form classes, grouped into logical sections.

**Rationale**: Explicit field rendering allows grouping fields into sections (Core Transaction → Context → Documentation), which improves readability beyond simple field reordering. Bootstrap 5's grid system (`.row`/`.col-md-6`) enables responsive side-by-side layout for related fields.

**Alternatives considered**:
- Using `{{ form.as_p }}` — quick but provides no control over grouping or responsive layout.
- Using django-crispy-forms — adds a dependency for a simple layout change.

## 3. No Data Model Changes

**Decision**: No schema changes needed.

**Rationale**: The feature only changes field display order. The Payment model, all field types, validators, and database schema remain untouched.

## 4. No View Logic Changes

**Decision**: View code in `payments/views.py` needs no modification.

**Rationale**: The view creates a `PaymentForm` instance, validates it, and saves it — none of this depends on field display order. The form's `cleaned_data` dict is field-name-keyed, not position-dependent.
