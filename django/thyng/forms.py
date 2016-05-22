from django import forms
from django.contrib.auth.forms import AuthenticationForm \
    as BaseAuthenticationForm
from django.utils.translation import ugettext as _

from registration.forms import RegistrationFormUniqueEmail

from .models import Project


class ThyngLayoutForm(object):
    def as_table(self):
        return self._html_output(
            normal_row=('<tr%(html_class_attr)s><th>%(label)s</th>'
                        '<td>%(field)s</td>'
                        '<td>%(errors)s%(help_text)s</td></tr>'),
            error_row='<tr><th></th><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<span class="helptext">%s</span>',
            errors_on_separate_row=False)


class ProjectCreateForm(ThyngLayoutForm, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'slug', 'description']


class AuthenticationForm(ThyngLayoutForm, BaseAuthenticationForm):
    pass


class RegistrationForm(ThyngLayoutForm, RegistrationFormUniqueEmail):

    username = forms.CharField(required=True)
    full_name = forms.CharField(required=False,
                                label=_("Full Name"),
                                help_text=_("(optional)"))
    email = forms.EmailField(required=True)
    password2 = forms.CharField(label=_("Confirm password"),
                                widget=forms.PasswordInput,
                                strip=False)

    class Meta(RegistrationFormUniqueEmail.Meta):
        fields = [
            'username',
            'full_name',
            'email',
            'password1',
            'password2'
        ]
        required_css_class = 'required'
