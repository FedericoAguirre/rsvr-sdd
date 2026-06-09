from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home_redirect(request):
    return redirect("reservation-list")


urlpatterns = [
    path("", home_redirect, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("clients/", include("apps.clients.urls")),
    path("reservations/", include("apps.reservations.urls")),
    path("equipment/", include("apps.equipment.urls")),
    path("classes/", include("apps.classes.urls")),
]
