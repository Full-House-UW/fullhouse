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

    def clean_expiration(self):
        expiration = self.cleaned_data['expiration']
        if expiration < date.today():
            raise forms.ValidationError("Please enter an expiration date in the future")
        return expiration

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

        self.fields['participants'] = forms.ModelMultipleChoiceField(
            queryset=housemembers,
            label='Participants (ctrl click to select multiple)'
        )

        # If we have an bound task, disable editing of first due
        # and replace it with a field to edit the next due
        task = getattr(self, 'instance', None)
        if task and task.id:
            self.fields['first_due'].widget = forms.HiddenInput()
            self.fields['first_due'].required = False

            due_name = 'next_due'
            due_label = 'Next Due'
            # store reference to next_due so we can update it on save
            self.next_instance = task.instances.latest('due_date')
            initial = self.next_instance.due_date
        else:
            due_name = 'first_due'
            due_label = 'First Due'
            initial = None

        self.fields[due_name] = forms.DateField(
            #initial=date.today(),
            initial=initial,
            label='%s (mm-dd-yyyy)' % due_label,
            widget=forms.widgets.DateInput(format='%m-%d-%Y'),
            input_formats=('%m-%d-%Y',),
        )

    def clean_first_due(self):
        # Disallow changing of first due field
        instance = getattr(self, 'instance', None)
        if instance and instance.first_due:
            return instance.first_due
        else:
            return self.cleaned_data.get('first_due', None)

    def save(self, commit=True):
        instance = super(CreateTaskForm, self).save(commit=commit)

        # save the updated next due date
        next_due = self.cleaned_data.get('next_due', None)
        if next_due:
            self.next_instance.due_date = next_due
            self.next_instance.save()

        return instance


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'house')

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    birthday = forms.DateField(
        widget=forms.widgets.DateInput(format='%m-%d-%Y'),
        input_formats=('%m-%d-%Y',),
        required=False,
        label='Birthday (mm-dd-yyyy):'
    )

    def save(self, commit=True):
        instance = super(UpdateUserForm, self).save(commit=commit)
        user = instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return instance
