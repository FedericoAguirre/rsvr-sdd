from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["client", "equipment", "class_slot", "date", "created_by"]
    list_filter = ["date", "class_slot"]
    search_fields = ["client__first_name", "client__last_name", "client__email"]
