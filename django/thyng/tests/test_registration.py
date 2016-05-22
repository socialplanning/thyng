from django.test import TestCase
from django.utils.translation import ugettext as _
import lxml.html

from ..forms import RegistrationForm


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
