from djangohelpers.lib import rendered_with, allow_http

@allow_http("GET")
@rendered_with("thyng/home.html")
def home(request):
    return {}

