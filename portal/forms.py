from django import forms

from .models import BlogPost, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "slug", "summary", "description", "thumbnail", "is_public"]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "slug", "summary", "content", "thumbnail", "is_public"]
