from django.contrib import admin
from .models import ClassSlot


@admin.register(ClassSlot)
class ClassSlotAdmin(admin.ModelAdmin):
    list_display = ["day_of_week", "time", "is_active"]
    list_filter = ["is_active"]
    ordering = ["day_of_week", "time"]
