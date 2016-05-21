from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^$', views.home, name='home'),

    url('^login/$', views.home, name='login'),
    url('^join/$', views.home, name='join'),

    url('^projects/(?P<slug>[0-9a-zA-Z\-\_]+)/$', views.project_home,
        name='project_home'),
]
