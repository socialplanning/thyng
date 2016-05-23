from djangohelpers.lib import rendered_with, allow_http
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .forms import ProjectCreateForm
from .models import Project, ProjectMember, ProjectFeaturelet


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


@allow_http("GET", "POST")
def featurelet(request, slug, featurelet, path):
    featurelet = get_object_or_404(ProjectFeaturelet,
                                   project__slug=slug,
                                   slug=featurelet)

    resp = HttpResponse(status=305)
    resp['Location'] = featurelet.proxy
    resp['X-Thyng-Container-Url'] = reverse('project_home', args=[slug])
    resp['X-Thyng-Featurelet-Slug'] = featurelet.slug
    resp['X-Thyng-Featurelet-Instance'] = featurelet.instance
    resp['X-Thyng-Path-Info'] = path
    return resp


@allow_http("GET", "POST")
@rendered_with("thyng/create_project.html")
def create_project(request):
    if request.user.is_anonymous():
        return redirect(reverse("auth_login"))

    form = ProjectCreateForm(data=request.POST or None)

    if request.method == "GET" or not form.is_valid():
        return {
            'form': form
        }

    project = form.save(commit=False)
    project.creator = request.user
    project.save()

    ProjectMember(project=project, user=request.user,
                  role=Project.ADMIN_ROLE).save()

    return redirect(reverse('project_home', args=[project.slug]))
