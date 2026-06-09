from django.urls import path
from . import views

app_name = "reservations"
urlpatterns = [
    path("", views.reservation_list, name="reservation-list"),
    path("create/", views.reservation_create, name="reservation-create"),
    path("<int:pk>/", views.reservation_detail, name="reservation-detail"),
]
