from django.urls import path

from . import views

app_name = "classes"
urlpatterns = [
    path("", views.class_schedule, name="class-schedule"),
    path("<int:pk>/toggle/", views.class_toggle, name="class-toggle"),
    path("prices/", views.ClassPricesView.as_view(), name="price-list"),
    path("prices/add/", views.ClassPriceCreateView.as_view(), name="price-add"),
]
