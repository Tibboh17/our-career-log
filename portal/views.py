from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import bleach
import markdown
from uuid import uuid4

from .forms import BlogPostForm, ProjectForm
from .models import BlogPost, Project

def home(request):
    """Render the public project landing page."""
    public_count = Project.objects.filter(is_public=True).count()
    context = {
        "public_count": public_count,
    }
    return render(request, "portal/index.html", context)


def _render_markdown(text):
    rendered = markdown.markdown(
        text or "",
        extensions=["fenced_code", "tables", "nl2br"],
    )
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
        {
            "p",
            "pre",
            "code",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "br",
            "hr",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "blockquote",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "a",
            "img",
        }
    )
    allowed_attrs = {
        "a": ["href", "title", "target", "rel"],
        "img": ["src", "alt", "title"],
        "th": ["align"],
        "td": ["align"],
    }
    rendered = bleach.clean(
        rendered,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=["http", "https", "mailto"],
    )
    return bleach.linkify(rendered)


def project_list(request):
    """Render the public project list page."""
    projects = (
        Project.objects.filter(is_public=True)
        .order_by("-created_at")
    )
    context = {
        "projects": projects,
    }
    return render(request, "portal/projects.html", context)


def project_detail(request, slug):
    """Render a public project detail page."""
    project = get_object_or_404(
        Project.objects.filter(is_public=True),
        slug=slug,
    )
    rendered_description = _render_markdown(project.description)
    context = {
        "project": project,
        "rendered_description": rendered_description,
    }
    return render(request, "portal/detail.html", context)


def _staff_only(user):
    return user.is_authenticated and user.is_staff


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("portal:project-list")
    else:
        form = ProjectForm()
    context = {
        "form": form,
    }
    return render(request, "portal/project_form.html", context)


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def project_manage(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "portal/project_manage.html", {"projects": projects})


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def project_edit(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("portal:project-manage")
    else:
        form = ProjectForm(instance=project)
    return render(request, "portal/project_form.html", {"form": form, "edit_mode": True})


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        project.delete()
        return redirect("portal:project-manage")
    return render(request, "portal/project_delete.html", {"project": project})


def blog_list(request):
    posts = BlogPost.objects.filter(is_public=True).order_by("-created_at")
    return render(request, "portal/blog_list.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.filter(is_public=True), slug=slug)
    rendered_content = _render_markdown(post.content)
    return render(
        request,
        "portal/blog_detail.html",
        {"post": post, "rendered_content": rendered_content},
    )


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def blog_manage(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "portal/blog_manage.html", {"posts": posts})


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def blog_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("portal:blog-manage")
    else:
        form = BlogPostForm()
    return render(request, "portal/blog_form.html", {"form": form})


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def blog_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("portal:blog-manage")
    else:
        form = BlogPostForm(instance=post)
    return render(request, "portal/blog_form.html", {"form": form, "edit_mode": True})


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("portal:blog-manage")
    return render(request, "portal/blog_delete.html", {"post": post})


@login_required(login_url="/admin/login/")
@user_passes_test(_staff_only, login_url="/admin/login/")
def upload_markdown_image(request):
    if request.method != "POST" or "image" not in request.FILES:
        return JsonResponse({"error": "invalid_request"}, status=400)
    image = request.FILES["image"]
    if not image.content_type or not image.content_type.startswith("image/"):
        return JsonResponse({"error": "invalid_type"}, status=400)
    extension = image.name.rsplit(".", 1)[-1] if "." in image.name else "png"
    filename = f"{uuid4().hex}.{extension}"
    upload_path = "markdown_uploads"
    storage_path = f"{upload_path}/{filename}"
    from django.core.files.storage import default_storage

    saved_path = default_storage.save(storage_path, image)
    url = default_storage.url(saved_path)
    return JsonResponse({"url": url})
