"""API routes for payment receipt exports."""

from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/receipt/", views.payment_receipt, name="receipt"),
    path(
        "<int:pk>/receipt/markdown/",
        views.payment_receipt_markdown,
        name="receipt-markdown",
    ),
]
