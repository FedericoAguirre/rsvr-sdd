# Contracts: Payments Client Search

## Modified Endpoint

### GET /payments/

**Existing behavior**: Returns paginated list of payments. Supports `?client=<id>` to filter by client ID.

**New behavior**: Adds `?q=<search-term>` parameter for client name/email/mobile search.

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | No | Search term for client name, email, or mobile. Minimum 3 characters to trigger name search |
| `page` | integer | No | Page number for pagination |

### Response

Renders `payments/payment_list.html` template with context:

| Context Variable | Type | Description |
|------------------|------|-------------|
| `payments` | QuerySet | Filtered payment list (or all if no q) |
| `page_obj` | Page | Paginated page object |
| `client_filter` | string | Current search term (replaces previous numeric client ID) |
| `not_found` | bool | True when q is set but no payments match |

### HTMX Request

When `HX-Request` header is present, renders only `payments/partials/_payment_search_results.html` instead of the full page.

### Implementation Notes

- Search query: `Client.objects.filter(is_active=True).filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q) | Q(mobile__icontains=q)).values_list("id", flat=True)`
- Payment filter: `Payment.objects.filter(client_id__in=matching_client_ids, is_deleted=False)`
- If `q` is empty or `< 3` chars: return all payments (no filter)
- Pagination links must preserve `?q=` parameter
