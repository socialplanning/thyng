from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


User = settings.AUTH_USER_MODEL


class Project(models.Model):

    ADMIN_ROLE = 'admin'
    USER_ROLE = 'user'
    NONMEMBER_ROLE = None

    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.slug

    def nav_entries(self):
        return [
            {"href": "", "title": _("Summary")},
            {"href": "", "title": _("Team")},
            {"href": "", "title": _("Contents")},
            {"href": "", "title": _("Manage Team"), "roles": [Project.ADMIN_ROLE]},
            {"href": "", "title": _("Preferences"), "roles": [Project.ADMIN_ROLE]},
            {"href": "", "title": _("Join Project"), "roles": [Project.NONMEMBER_ROLE]},
        ]

class ProjectMember(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    created_at = models.DateTimeField(auto_now_add=True)

    role = models.CharField(max_length=255, choices=[
        (Project.USER_ROLE, _("Member")),
        (Project.ADMIN_ROLE, _("Admin")),
    ])
