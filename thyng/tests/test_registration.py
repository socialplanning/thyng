from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.translation import ugettext as _
import lxml.html
import re

from ..forms import RegistrationForm
from ..registration_backend import RegistrationAuthBackend

from .factories import UserFactory


User = get_user_model()


class BackendTest(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_backend(self):
        backend = RegistrationAuthBackend()
        self.assertEqual(self.user, backend.get_user(1))
        self.assertEqual(None, backend.get_user(2))

        self.assertEqual(
            None, backend.authenticate(username='fakeuser'))
        self.assertEqual(
            None,
            backend.authenticate(username=self.user.username))
        self.assertEqual(
            None,
            backend.authenticate(username='fakeuser',
                                 from_activation_view=True))
        self.assertEqual(
            self.user,
            backend.authenticate(username=self.user.username,
                                 from_activation_view=True))


class BasicTest(TestCase):

    def test_registration_form_layout(self):
        form = RegistrationForm()
        rsp = lxml.html.fromstring(form.as_table())

        # Help text + errors are in its own column
        self.assertEqual(2, len(rsp.cssselect("tr")[0].cssselect("td")))

        name_row = [row for row in rsp.cssselect("tr")
                    if 'id_full_name' in lxml.html.tostring(row)][0]
        self.assertIn(_("(optional)"),
                      lxml.html.tostring(name_row.cssselect("td")[-1]))

        form = RegistrationForm(data={
            'username': 'lammy',
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertNotIn("full_name", form.errors)

        rsp = lxml.html.fromstring(form.as_table())
        self.assertEqual(1, len(
            rsp.cssselect("tr")[-1].cssselect("td .errorlist")))


class RegistrationTest(TestCase):

    def setUp(self):
        self.username = 'lammy'
        self.password = 's3kr3tp455w0rd!'
        self.join_url = reverse('registration_register')

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_registration_workflow(self):

        self.assertEqual(0, len(mail.outbox))

        rsp = self.client.post(self.join_url, data={
            'username': self.username,
            'email': 'lammy@example.com',
            'password1': self.password,
            'password2': self.password,
        })
        self.assertRedirects(rsp, reverse('registration_complete'))

        self.assertEqual(1, len(mail.outbox))

        email = str(mail.outbox[0].message())
        self.assertIn('/confirm-account/', email)

        user = User.objects.get(username='lammy')
        self.assertEqual(False, user.is_active)

        key = re.search('/confirm-account/(.*)/', email).groups()[0]
        confirm = reverse('registration_activate', args=[key])
        rsp = self.client.get(confirm)
        self.assertRedirects(
            rsp, reverse('registration_activation_complete'))

        user = User.objects.get(username='lammy')
        self.assertEqual(True, user.is_active)
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            user.pk)
