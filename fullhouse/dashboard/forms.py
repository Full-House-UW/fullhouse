from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib.auth.models import User
from emailusernames.utils import user_exists

import models


class CreateHouseForm(forms.ModelForm):
    class Meta:
        model = models.House


class AddMemberForm(forms.Form):
    email = forms.EmailField(required=True)


class BaseAddMemberFormSet(BaseFormSet):
    def clean(self):
        super(BaseAddMemberFormSet, self).clean()
        if not self.has_changed():
            raise forms.ValidationError("At least one email required")


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = models.Announcement
        exclude = ('creator', 'house')


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ('creator', 'house')

    def __init__(self, *args, **kwargs):
        members = kwargs.pop('members')
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned'].queryset = members

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ('user', 'house')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    #email = forms.EmailField()

    #def clean(self):
    #    cleaned_data = super(UpdateUserForm, self).clean()
    #    email = cleaned_data.get('email')
    #    if self.user.email != email and user_exists(email):
    #        raise forms.ValidationError(
    #            "Another user with that email exists"
    #        )
    #    return cleaned_data
