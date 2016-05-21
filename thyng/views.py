from djangohelpers.lib import rendered_with, allow_http

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
