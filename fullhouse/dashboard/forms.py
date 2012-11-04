from django import forms
from django.forms.formsets import BaseFormSet

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
