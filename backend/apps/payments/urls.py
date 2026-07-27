from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.PaymentListView.as_view(), name="list"),
    path("create/", views.PaymentCreateView.as_view(), name="create"),
    path(
        "from-reservation/", views.PaymentCreateView.as_view(),
        name="create_from_reservation",
    ),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PaymentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.PaymentDeleteView.as_view(), name="delete"),
    path("<int:pk>/associate/", views.PaymentAssociateView.as_view(), name="associate"),
    path(
        "client/<int:client_id>/", views.ClientPaymentHistoryView.as_view(),
        name="client_history",
    ),
    path("reports/", views.PaymentReportView.as_view(), name="reports"),
    path("reports/export/", views.PaymentExportView.as_view(), name="export"),
    path("<int:pk>/batch-data/", views.BatchDataView.as_view(), name="batch_data"),
    path("<int:pk>/batch-create/", views.BatchCreateView.as_view(), name="batch_create"),
    path("<int:pk>/calendar/", views.payment_calendar, name="calendar"),
]
