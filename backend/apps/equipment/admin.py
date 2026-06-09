from django.contrib import admin
from .models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["name", "equipment_type", "status", "created_at"]
    list_filter = ["status", "equipment_type"]
    search_fields = ["name"]
