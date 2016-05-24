from django.contrib.auth import authenticate, login
from registration import signals
from registration.backends.hmac.views import RegistrationView \
    as BaseRegistrationView

from .forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm


def log_in_activated_user(sender, **kwargs):
    user = kwargs['user']
    request = kwargs['request']

    user = authenticate(
        username=user.username, from_activation_view=True)
    login(request, user)

signals.user_activated.connect(log_in_activated_user)
