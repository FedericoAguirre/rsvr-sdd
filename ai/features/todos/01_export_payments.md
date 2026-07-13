# Export payments

## User story

As an Administrator, I want to download the payments data in a spreadsheet, so that I can analyze it outside the webpage.

## Acceptance criteria

Given I am on the payments reports page with a date range filter, when I select a range in "Fecha de inicio" and "Fecha de fin" and click Export, then a spreadsheet is downloaded containing only payments within that date range.

Given I export payments, when the file is downloaded, then it is in Excel format (.xlsx) with the filename `pagos_[start_date]_[end_date].xlsx` where dates are in YYYYMMDD format.

Given I open the downloaded file, when I view the spreadsheet, then it contains the columns: Identificador, Cliente, Monto, Tipo, Fecha, Clases.

Given there are no payments in the selected date range, when I click export, then an alert is shown indicating no data is available and no file is downloaded.

## Definition of Done

- Reuse the payments/reports webpage functionality, and views as much as possible,
    add the "Exportar" button next to the right of "Generar reporte" button.
- Code reviewed, tested in staging, downloaded file validated against database data.
