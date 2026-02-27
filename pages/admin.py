from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "contact", "message")
    ordering = ("-created_at",)
from django.contrib import admin

# Register your models here.
