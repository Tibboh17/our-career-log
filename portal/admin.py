from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_public", "created_at")
    list_filter = ("is_featured", "is_public", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
