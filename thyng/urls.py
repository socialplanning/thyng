from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^$', views.home),

    url('^login/$', views.home),
    url('^join/$', views.home),

    url('^projects/(?P<slug>[0-9a-zA-Z\-\_]+)/$', views.project_home,
        name='project_home'),
]
