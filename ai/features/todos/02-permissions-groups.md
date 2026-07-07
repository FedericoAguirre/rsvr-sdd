# 2. Create permissions for 2 groups: Administrators and Operators

As a developer I want to add 2 groups to this web app: Administrators and
Operators.

I want the Administrators and the Operators to have a role based access.

I want this access to be programmatically created.

The Administrators can access to ALL the URLS and its sections listed in the "##
URLS" section.

The Operators can access to ALL the URLS, except the next sections:

### `payments` (app_name = "payments")
- `"<int:pk>/edit/"` → `views.PaymentUpdateView.as_view()` (name: `edit`)
- `"<int:pk>/delete/"` → `views.PaymentDeleteView.as_view()` (name: `delete`)
- `"reports/"` → `views.PaymentReportView.as_view()` (name: `reports`)


## URLS

### `classes` (app_name = "classes")
- `""` → `views.class_schedule` (name: `class-schedule`)
- `"<int:pk>/toggle/"` → `views.class_toggle` (name: `class-toggle`)

### `clients` (app_name = "clients")
- `"search/"` → `views.client_search` (name: `client-search`)
- `"create/"` → `views.client_create` (name: `client-create`)
- `"upload/"` → `views.client_csv_upload` (name: `client-csv-upload`)
- `"template/"` → `views.client_csv_template` (name: `client-csv-template`)
- `"<int:pk>/calendar/"` → `views.client_calendar` (name: `client-calendar`)
- `"<int:pk>/"` → `views.client_detail` (name: `client-detail`)

### `equipment` (app_name = "equipment")
- `""` → `views.equipment_list` (name: `equipment-list`)
- `"create/"` → `views.equipment_create` (name: `equipment-create`)
- `"<int:pk>/"` → `views.equipment_detail` (name: `equipment-detail`)
- `"<int:pk>/edit/"` → `views.equipment_edit` (name: `equipment-edit`)

### `payments` (app_name = "payments")
- `""` → `views.PaymentListView.as_view()` (name: `list`)
- `"create/"` → `views.PaymentCreateView.as_view()` (name: `create`)
- `"from-reservation/"` → `views.PaymentCreateView.as_view()` (name: `create_from_reservation`)
- `"<int:pk>/"` → `views.PaymentDetailView.as_view()` (name: `detail`)
- `"<int:pk>/edit/"` → `views.PaymentUpdateView.as_view()` (name: `edit`)
- `"<int:pk>/delete/"` → `views.PaymentDeleteView.as_view()` (name: `delete`)
- `"<int:pk>/associate/"` → `views.PaymentAssociateView.as_view()` (name: `associate`)
- `"client/<int:client_id>/"` → `views.ClientPaymentHistoryView.as_view()` (name: `client_history`)
- `"reports/"` → `views.PaymentReportView.as_view()` (name: `reports`)

### `reservations` (app_name = "reservations")
- `""` → `views.reservation_list` (name: `reservation-list`)
- `"pdf/"` → `views.reservation_list_pdf` (name: `reservation-list-pdf`)
- `"create/"` → `views.reservation_create` (name: `reservation-create`)
- `"<int:pk>/"` → `views.reservation_detail` (name: `reservation-detail`)
- `"<int:pk>/status/"` → `views.reservation_change_status` (name: `reservation-change-status`)
