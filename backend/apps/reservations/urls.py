from django.urls import path
from . import views

app_name = "reservations"
urlpatterns = [
    path("", views.reservation_list, name="reservation-list"),
    path("list/", views.reservation_list_by_slot, name="reservation-list-by-slot"),
    path("list/pdf/", views.reservation_list_pdf, name="reservation-list-pdf"),
    path("create/", views.reservation_create, name="reservation-create"),
    path("<int:pk>/", views.reservation_detail, name="reservation-detail"),
]
