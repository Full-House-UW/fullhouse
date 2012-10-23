from django.forms import ModelForm

import models


class CreateHouseForm(ModelForm):
    class Meta:
        model = models.House


class CreateAnnouncementForm(ModelForm):
    class Meta:
        model = models.Announcement
        exclude = ['creator', 'house']
