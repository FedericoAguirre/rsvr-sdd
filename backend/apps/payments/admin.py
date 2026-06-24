from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "payment_identifier", "client", "amount", "payment_type",
        "date", "class_slot_count", "is_deleted",
    ]
    list_filter = ["payment_type", "date", "is_deleted"]
    search_fields = ["payment_identifier", "client__first_name", "client__last_name"]
    readonly_fields = ["payment_identifier", "created_at", "updated_at"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "client", "amount", "payment_type", "payment_identifier",
                    "date", "class_slot_count",
                ],
            },
        ),
        (
            _("Optional"),
            {"fields": ["reference", "evidence", "notes"]},
        ),
        (
            _("Audit"),
            {"fields": ["created_by", "updated_by", "created_at", "updated_at"]},
        ),
        (
            _("Soft Delete"),
            {"fields": ["is_deleted", "deleted_at"]},
        ),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
