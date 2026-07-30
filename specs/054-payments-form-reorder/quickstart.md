# Quickstart Validation Guide: Reorder Payment Form Fields

**Purpose**: Run these validation scenarios to confirm the feature works end-to-end.

## Prerequisites

- Database running (`make db-up`)
- Dev server running (`make serve`)
- Staff user logged in

## Validation Scenarios

### Scenario 1: Field Order

Navigate to `/payments/create/` and verify fields appear in this exact order:

1. Cliente (dropdown)
2. Amount (numeric)
3. Cantidad de bloques de clase (numeric)
4. Tipo de pago (dropdown)
5. Fecha (date picker)
6. Notas (textarea)
7. Identificador de pago (text)
8. Referencia (text)
9. Comprobante (file upload)
10. Crear pago / Cancelar buttons

### Scenario 2: Tab Order

Press Tab repeatedly through the form. Focus must move through fields in the order listed above.

### Scenario 3: Form Submission

Fill out all required fields and click "Crear pago". Verify the payment is created and you're redirected to the payment detail page.

### Scenario 4: Validation Errors

Submit an empty form. Verify error messages appear below their respective fields.

### Scenario 5: Responsive Layout

- Desktop (>1024px): Amount and Cantidad de bloques side-by-side; Identificador and Referencia side-by-side
- Mobile (<768px): All fields stacked vertically

### Scenario 6: File Upload

Attach a file to Comprobante and submit. Verify the file uploads and displays correctly on the payment detail page.

## Data Model

No schema changes — see [data-model.md](data-model.md).

## Contracts

No interface contract changes — see [contracts/](contracts/).
