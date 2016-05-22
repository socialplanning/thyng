from djangohelpers.lib import rendered_with, allow_http
from django.shortcuts import get_object_or_404

from .models import Project


@allow_http("GET")
@rendered_with("thyng/home.html")
def home(request):

    newest_projects = list(Project.objects.order_by("-created_at")[:5])
    updated_projects = Project.objects.exclude(
        id__in=[i.id for i in newest_projects]).order_by("-updated_at")[:5]

    return {
        'newest_projects': newest_projects,
        'updated_projects': updated_projects,
    }


@allow_http("GET")
@rendered_with("thyng/project_home.html")
def project_home(request, slug):

    project = get_object_or_404(Project, slug=slug)

    return {
        'project': project
    }

@allow_http("GET")
@rendered_with("thyng/login.html")
def login(request):
    return {}

@allow_http("GET")
@rendered_with("thyng/join.html")
def join(request):
    return {}
