from django.test import TestCase

from .models import Project


class HomeViewVisibilityTests(TestCase):
    def test_home_shows_only_featured_public_projects(self):
        featured_project = Project.objects.create(
            title="Featured Project",
            is_public=True,
            is_featured=True,
        )
        Project.objects.create(
            title="Public Project",
            is_public=True,
            is_featured=False,
        )
        Project.objects.create(
            title="Featured Private Project",
            is_public=False,
            is_featured=True,
        )

        response = self.client.get("/")

        self.assertContains(response, featured_project.title)
        self.assertNotContains(response, "Public Project")
        self.assertNotContains(response, "Featured Private Project")

class ProjectListViewTests(TestCase):
    def test_project_list_shows_only_public_projects(self):
        public_project = Project.objects.create(
            title="Public Project",
            is_public=True,
            is_featured=False,
        )
        Project.objects.create(
            title="Private Project",
            is_public=False,
            is_featured=False,
        )

        response = self.client.get("/projects/")

        self.assertContains(response, public_project.title)
        self.assertNotContains(response, "Private Project")

    def test_project_list_search_filters_projects(self):
        Project.objects.create(
            title="Alpha Project",
            description="First project",
            is_public=True,
            is_featured=False,
        )
        Project.objects.create(
            title="Beta Project",
            description="Second project",
            is_public=True,
            is_featured=False,
        )

        response = self.client.get("/projects/")

        self.assertContains(response, "Alpha Project")
        self.assertContains(response, "Beta Project")
