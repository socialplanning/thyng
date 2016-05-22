from registration.backends.hmac.views import RegistrationView \
    as BaseRegistrationView

from .forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm
