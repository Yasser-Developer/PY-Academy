from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "created_at")
    list_filter = ("is_published", "published_at", "created_at")
    search_fields = ("title", "excerpt", "content", "slug")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at", "-created_at")
