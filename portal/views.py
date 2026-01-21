from django.db.models import Prefetch
from django.shortcuts import render

from .models import Artifact, Project

def home(request):
    """Render the public project landing page."""
    public_artifacts = Prefetch(
        "artifacts",
        queryset=Artifact.objects.filter(is_public=True).order_by("-created_at"),
    )
    projects = (
        Project.objects.filter(is_public=True)
        .order_by("-created_at")
        .prefetch_related(public_artifacts)
    )
    context = {
        "projects": projects,
    }
    return render(request, "portal/index.html", context)
