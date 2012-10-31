from django import forms
from django.forms.extras.widgets import SelectDateWidget
from registration.forms import RegistrationForm

#class LoginForm(forms.Form):
#    username = forms.CharField(max_length=30)
#    password = forms.CharField( widget=forms.PasswordInput, label="Your Password" )

class FullhouseRegistrationForm(RegistrationForm):
    # inherit all fields of RegistrationForm and add our own
    birthday = forms.DateField(widget=SelectDateWidget)

