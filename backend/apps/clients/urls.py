from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path("search/", views.client_search, name="client-search"),
    path("create/", views.client_create, name="client-create"),
    path("upload/", views.client_csv_upload, name="client-csv-upload"),
    path("template/", views.client_csv_template, name="client-csv-template"),
    path("<int:pk>/", views.client_detail, name="client-detail"),
]
