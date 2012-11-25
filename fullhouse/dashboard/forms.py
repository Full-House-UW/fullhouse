from datetime import (
    date, timedelta
)
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

    def __init__(self, *args, **kwargs):
        super(CreateAnnouncementForm, self).__init__(*args, **kwargs)
        self.fields['expiration'] = forms.DateField(
            widget=forms.widgets.DateInput(format='%m-%d-%Y'),
            input_formats=('%m-%d-%Y',),
        )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ('creator', 'house')

    def __init__(self, *args, **kwargs):
        housemembers = kwargs.pop('members')
        super(CreateTaskForm, self).__init__(*args, **kwargs)

        self.fields['description'].required = False
        self.fields['frequency'].required = False
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

    #def clean(self):15323
    #    cleaned_data = super(CreateTaskForm, self).clean()
    #    if datetime.now < cleaned_data['first_due']:
    #        raise forms.ValidationError(
    #            "Cannot set first due date in the past"
    #        )
    #    return cleaned_data


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
