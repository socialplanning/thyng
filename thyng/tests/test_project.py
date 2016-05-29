from django.test import TestCase
from django.core.urlresolvers import reverse
import lxml.html

from ..models import Project, ProjectMember
from .factories import UserFactory, ProjectFactory, ProjectMemberFactory


class BasicTest(TestCase):

    def setUp(self):
        self.create = reverse('create_project')
        self.password = 'a p4ssword!'
        self.user = UserFactory(password=self.password)

    def test_create_project_anonymous(self):
        rsp = self.client.get(self.create)
        self.assertRedirects(rsp, reverse('auth_login'))

    def test_create_project_loggedin(self):
        self.assertEqual(0, Project.objects.all().count())
        self.client.login(username=self.user.username, password=self.password)

        rsp = self.client.get(self.create)
        self.assertEqual(200, rsp.status_code)

        rsp = self.client.post(self.create, data={
            'title': "Project One",
            'slug': "project-one",
        })

        self.assertEqual(1, Project.objects.all().count())
        project = Project.objects.all()[0]

        self.assertRedirects(rsp, reverse('project_home', args=[project.slug]))
        self.assertEqual(project.title, 'Project One')

        self.assertEqual(1, ProjectMember.objects.all().count())
        self.assertEqual(1, project.projectmember_set.count())

        member = project.projectmember_set.all()[0]
        self.assertEqual(member.user, self.user)
        self.assertEqual(member.role, Project.ADMIN_ROLE)
        self.assertEqual(project.creator, self.user)

        self.assertEqual(unicode(project), 'project-one')

    def test_project_topnav(self):
        project = ProjectFactory(creator=self.user)
        member = ProjectMemberFactory(user=self.user, project=project,
                                      role=Project.ADMIN_ROLE)
        self.client.login(username=self.user.username, password=self.password)

        self.assertContains(self.client.get('/'), 'Start a Project')

        home = reverse('project_home', args=[project.slug])
        rsp = self.client.get(home)

        self.assertNotContains(rsp, 'Start a Project')
        self.assertContains(rsp, 'Summary')
        self.assertContains(rsp, 'Manage Team')
        self.assertNotContains(rsp, 'Join Project')

        self.client.logout()
        rsp = self.client.get(home)
        self.assertNotContains(rsp, 'Start a Project')
        self.assertContains(rsp, 'Summary')
        self.assertNotContains(rsp, 'Manage Team')
        self.assertContains(rsp, 'Join Project')
