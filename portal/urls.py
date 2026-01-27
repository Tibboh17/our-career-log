from django.urls import path

from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.project_list, name="project-list"),
    path("projects/new/", views.project_create, name="project-create"),
    path("projects/upload-image/", views.upload_markdown_image, name="project-upload-image"),
    path("projects/manage/", views.project_manage, name="project-manage"),
    path("projects/<slug:slug>/edit/", views.project_edit, name="project-edit"),
    path("projects/<slug:slug>/delete/", views.project_delete, name="project-delete"),
    path("projects/<slug:slug>/", views.project_detail, name="project-detail"),
    path("blog/", views.blog_list, name="blog-list"),
    path("blog/manage/", views.blog_manage, name="blog-manage"),
    path("blog/new/", views.blog_create, name="blog-create"),
    path("blog/<slug:slug>/edit/", views.blog_edit, name="blog-edit"),
    path("blog/<slug:slug>/delete/", views.blog_delete, name="blog-delete"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog-detail"),
]
