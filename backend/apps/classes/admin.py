from django.contrib import admin

from .models import ClassPrice, ClassSlot


@admin.register(ClassSlot)
class ClassSlotAdmin(admin.ModelAdmin):
    list_display = ["day_of_week", "time", "is_active"]
    list_filter = ["is_active"]
    ordering = ["day_of_week", "time"]


@admin.register(ClassPrice)
class ClassPriceAdmin(admin.ModelAdmin):
    list_display = [
        "class_slot",
        "price",
        "current",
        "created_by",
        "created_at",
        "changed_at",
        "changed_by",
    ]
    list_filter = ["current", "created_at", "changed_at"]
    search_fields = ["class_slot__day_of_week", "class_slot__time"]
    readonly_fields = [
        "price",
        "class_slot",
        "current",
        "created_by",
        "created_at",
        "changed_at",
        "changed_by",
        "updated_at",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
