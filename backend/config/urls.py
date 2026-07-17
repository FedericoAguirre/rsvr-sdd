from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_redirect(request):
    return redirect("clients:client-search")


urlpatterns = [
    path("", home_redirect, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("clients/", include("apps.clients.urls")),
    path("reservations/", include("apps.reservations.urls")),
    path("equipment/", include("apps.equipment.urls")),
    path("classes/", include("apps.classes.urls")),
    path("payments/", include("apps.payments.urls")),
]
