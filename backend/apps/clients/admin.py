from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "mobile", "is_active"]
    search_fields = ["first_name", "last_name", "email", "mobile"]
    list_filter = ["is_active"]
