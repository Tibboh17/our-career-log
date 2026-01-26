from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Artifact, Project

def home(request):
    """Render the public project landing page."""
    public_artifacts = Prefetch(
        "artifacts",
        queryset=Artifact.objects.filter(is_public=True).order_by("-created_at"),
    )
    projects = (
        Project.objects.filter(is_public=True, is_featured=True)
        .order_by("-created_at")
        .prefetch_related(public_artifacts)
    )
    context = {
        "projects": projects,
    }
    return render(request, "portal/index.html", context)


def project_list(request):
    """Render the public project list page."""
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
    return render(request, "portal/projects.html", context)


def project_detail(request, pk):
    """Render a public project detail page."""
    public_artifacts = Prefetch(
        "artifacts",
        queryset=Artifact.objects.filter(is_public=True).order_by("-created_at"),
    )
    project = get_object_or_404(
        Project.objects.filter(is_public=True).prefetch_related(public_artifacts),
        pk=pk,
    )
    context = {
        "project": project,
    }
    return render(request, "portal/detail.html", context)
