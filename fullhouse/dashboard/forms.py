from django import forms

class AnnouncementForm(forms.Form):
    title = forms.CharField(max_length=30)
    text = forms.CharField(widget=forms.Textarea);
