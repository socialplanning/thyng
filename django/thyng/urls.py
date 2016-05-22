from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .forms import AuthenticationForm
from .registration_views import RegistrationView
from registration.backends.hmac.views import ActivationView
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('^$', views.home, name='home'),

    url(r'^activate/(?P<activation_key>[-:\w]+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^join/$',
        RegistrationView.as_view(),
        name='registration_register'),
    url(r'^login/$',
        auth_views.login, {'template_name': 'registration/login.html',
                           'authentication_form': AuthenticationForm},
        name='auth_login'),

    url('^projects/create/$', views.create_project,
        name='create_project'),
    url('^projects/(?P<slug>[0-9a-zA-Z\-\_]+)/$', views.project_home,
        name='project_home'),
]
