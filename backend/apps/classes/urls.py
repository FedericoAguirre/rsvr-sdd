from django.urls import path

from . import views

app_name = "classes"
urlpatterns = [
    path("", views.class_schedule, name="class-schedule"),
    path("<int:pk>/toggle/", views.class_toggle, name="class-toggle"),
    path("<int:pk>/prices/", views.ClassPricesView.as_view(), name="class-prices"),
    path(
        "<int:pk>/prices/add/",
        views.ClassPriceCreateView.as_view(),
        name="class-price-add",
    ),
]
