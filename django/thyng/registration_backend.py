from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationAuthBackend(object):

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self,
                     username=None, from_activation_view=False):
        if not from_activation_view:
            return None

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
