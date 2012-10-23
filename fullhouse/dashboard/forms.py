from django import forms

class AnnouncementForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=30)
    text = forms.CharField(widget=forms.Textarea, min_length=1);
