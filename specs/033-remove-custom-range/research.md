# Research: Remove Custom Range

## Research Tasks

1. **Confirm `range` and `day` grouping are functionally identical** — verify no unique logic exists under the `range` branch
2. **Identify all references to `range` in views, templates, tests, and locale files**

---

## Decision 1: `range` and `day` are identical

**Decision**: Remove the `range` branch entirely. The `range` grouping code path:

```python
elif grouping == "range":
    rows = qs.values("date", "payment_type").annotate(
        total=Sum("amount"), count=Count("id"),
    ).order_by("date", "payment_type")
```

is byte-for-byte identical to the `day` path. No unique logic or custom ordering exists under `range`.

**Rationale**: Removing dead code with zero behavioral impact.

---

## Decision 2: Graceful fallback via `get()`

**Decision**: Replace the `grouping == "range"` elif with a fallback in the `get()` call. Using `self.request.GET.get("grouping", "month")` means any unrecognized value (including `range`) will be ignored and `"month"` will be used as default — the current default value for the template.

**Rationale**: No need for an explicit `range` handler. The Django template will continue to show the dropdown with only Day/Week/Month options. The `grouping` variable in the template context will still hold the submitted value, but the backend will default to month rendering.

**Alternatives considered**:
- **Explicit `if grouping == "range": grouping = "month"` check**: More defensive but unnecessary — let the `get()` default handle it.

---

## Decision 3: i18n cleanup

**Decision**: Remove the `msgid "Custom Range"` entry from `django.po` to keep translations clean.

**Rationale**: Dead translation entries should not accumulate. This is in line with code quality principles.
