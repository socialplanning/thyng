from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import ProjectFactory


class BasicTest(TestCase):

    def test_homepage(self):
        rsp = self.client.get("/")
        self.assertEqual(200, rsp.status_code)
        self.assertIn("Thyng", rsp.content)

    def test_newest_project(self):
        project = ProjectFactory()
        rsp = self.client.get("/")
        self.assertIn(project.title, rsp.content)

    def test_updated_project(self):
        """
        Items in 'newest projects' are excluded from 'updated projects'
        """
        projects = []
        while len(projects) < 11:
            projects.append(ProjectFactory())
        rsp = self.client.get("/")

        self.assertNotIn(projects[0].title, rsp.content)
        for project in projects[1:]:
            self.assertIn(project.title, rsp.content)

    def test_project_homepage(self):
        project = ProjectFactory()
        rsp = self.client.get(reverse('project_home', args=[project.slug]))
        self.assertEqual(200, rsp.status_code)
