from django.contrib import admin

from .models import Artifact, Project

class ArtifactInline(admin.TabularInline):
    model = Artifact
    extra = 0
    fields = ("title", "is_public", "external_url", "file", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_public", "created_at")
    list_filter = ("is_featured", "is_public", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    inlines = [ArtifactInline]

@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "is_public", "created_at")
    list_filter = ("is_public", "created_at")
    search_fields = ("title", "description", "project__title")
    ordering = ("-created_at",)
