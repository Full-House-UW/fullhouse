from datetime import (
    date, timedelta
)
from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
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

    def __init__(self, *args, **kwargs):
        super(CreateAnnouncementForm, self).__init__(*args, **kwargs)
        self.fields['expiration'] = forms.DateField(
            widget=forms.widgets.DateInput(format='%m-%d-%Y'),
            input_formats=('%m-%d-%Y',),
        )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ('is_active', 'creator', 'house')

    def __init__(self, *args, **kwargs):
        housemembers = kwargs.pop('members')
        super(CreateTaskForm, self).__init__(*args, **kwargs)

        self.fields['description'].required = False
        self.fields['first_due'] = forms.DateField(
            #initial=date.today(),
            widget=forms.widgets.DateInput(format='%m-%d-%Y'),
            input_formats=('%m-%d-%Y',),
        )
        self.fields['participants'] = forms.ModelMultipleChoiceField(
            queryset=housemembers
        )

        # Disallow changing of first_due field, except at creation
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['first_due'].widget.attrs['disabled'] = True
            self.fields['first_due'].required = False

    def clean_first_due(self):
        # Disallow changing of first due field
        instance = getattr(self, 'instance', None)
        if instance and instance.first_due:
            return instance.first_due
        else:
            return self.cleaned_data.get('first_due', None)


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'house')

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    birthday = forms.DateField(
        widget=forms.widgets.DateInput(format='%m-%d-%Y'),
        input_formats=('%m-%d-%Y',),
        required=False
    )

    def save(self, commit=True):
        instance = super(UpdateUserForm, self).save(commit=commit)
        user = instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return instance
