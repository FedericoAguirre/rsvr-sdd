from django.urls import path

from . import views

app_name = "equipment"
urlpatterns = [
    path("", views.equipment_list, name="equipment-list"),
    path("create/", views.equipment_create, name="equipment-create"),
    path("<int:pk>/", views.equipment_detail, name="equipment-detail"),
    path("<int:pk>/edit/", views.equipment_edit, name="equipment-edit"),
]
