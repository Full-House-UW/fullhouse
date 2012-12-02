import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from emailusernames.forms import EmailUserCreationForm
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import forms as auth_forms

MIN_LENGTH = 6


def _clean_password(self, fieldname):
    password = self.cleaned_data[fieldname]
    if len(password) < MIN_LENGTH:
        raise forms.ValidationError(
            _("Password must be at least %d characters long." % MIN_LENGTH)
        )
    return password


class FullhouseRegistrationForm(EmailUserCreationForm):

    def clean_password1(self):
        return _clean_password(self, 'password1')


class SetPasswordForm(auth_forms.SetPasswordForm):

    def clean_new_password1(self):
        return _clean_password(self, 'new_password1')


class PasswordChangeForm(auth_forms.PasswordChangeForm):

    def clean_new_password1(self):
        return _clean_password(self, 'new_password1')
