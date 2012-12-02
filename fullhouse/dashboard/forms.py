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
