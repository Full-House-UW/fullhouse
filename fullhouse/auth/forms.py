import datetime
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from registration.forms import RegistrationForm


class FullhouseRegistrationForm(RegistrationForm):
    # inherit all fields of RegistrationForm and add our own
    birthday = forms.DateField(required=False)
