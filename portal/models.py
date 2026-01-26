from django.db import models

class Project(models.Model):
    """Project entry shown on the portfolio site."""

    # Core content
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Visibility and timestamps
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Artifact(models.Model):
    """File or link attached to a project."""

    # Relations
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="artifacts")

    # Core content
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="artifacts/", blank=True, null=True)
    external_url = models.URLField(blank=True)

    # Visibility and timestamps
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
