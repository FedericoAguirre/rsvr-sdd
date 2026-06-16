from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path("search/", views.client_search, name="client-search"),
    path("create/", views.client_create, name="client-create"),
    path("<int:pk>/", views.client_detail, name="client-detail"),
]
