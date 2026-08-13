# Research: Payment Receipt Export

## Decision: Reuse ReportLab for in-memory PDF generation

**Rationale**: ReportLab is already a project dependency and the reservations PDF implementation already uses Platypus `SimpleDocTemplate`, `Paragraph`, `Table`, and `TableStyle`. The documented Platypus flow supports automatic layout and pagination, while `BytesIO` allows the response to remain a direct binary download without temporary files.

**Alternatives considered**: Introducing an HTML-to-PDF renderer was rejected because it adds a dependency and duplicates an existing project convention. A task queue was deferred because the defined primary volume is 50 reservations and the feature requires an immediate browser download.

## Decision: Share one normalized receipt projection between PDF and Markdown

**Rationale**: A single projection of payment, client, and linked reservation values prevents the two formats from drifting. It also provides one place for active-language labels, `DD/MM/YYYY` dates, optional equipment handling, and the no-reservations message.

**Alternatives considered**: Building Markdown in browser JavaScript was rejected because it would duplicate formatting and localization rules and could expose inconsistent data compared with the PDF endpoint.

## Decision: Add protected API routes separate from HTML payment routes

**Rationale**: The required PDF contract is `/api/payments/{id}/receipt`; the existing application reserves `/payments/` for server-rendered pages. The PDF route returns `application/pdf` with an attachment filename, and a sibling Markdown route returns copyable text using the same receipt projection.

**Alternatives considered**: Adding a query parameter to the PDF route was rejected because content negotiation between binary PDF and Markdown would make the primary contract less explicit. Embedding all receipt data in the detail template was rejected because it duplicates server response logic and complicates fallback behavior.

## Decision: Use authentication and payment-detail access as the authorization boundary

**Rationale**: Existing payment detail, calendar, and export flows use authenticated Django views. The receipt endpoint must require the same authenticated operator context, retrieve only the requested payment, and return a not-found response for missing records without leaking data.

**Alternatives considered**: Adding a new permission model was rejected because the specification scopes access to operators who already can view payment details and the project has no separate receipt permission requirement.

## Decision: Sanitize filenames by preserving accented letters and replacing unsafe characters

**Rationale**: This follows the clarification and supports Spanish names while preventing common filesystem failures. The payment identifier remains the preferred reference; the payment primary key is the deterministic fallback when the optional reference is empty.

**Alternatives considered**: ASCII transliteration was rejected because the clarified requirement preserves accented letters. Blocking downloads without a reference was rejected because every persisted payment has a unique ID.

## Documentation Basis

- Django documentation: `LoginRequiredMixin`/`login_required` for protected views and Django HTTP response/header utilities.
- ReportLab documentation: Platypus document stories, tables, pagination, and TrueType font registration for Unicode text.
- pytest-django documentation: explicit database marks/fixtures for authenticated integration tests.
- Repository evidence: `backend/apps/reservations/views.py` already generates PDFs with ReportLab and `backend/tests/test_reservations_list.py` extracts PDF text with pdfminer.six.
