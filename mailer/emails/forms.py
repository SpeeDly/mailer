from django import forms
from mailer.utils.forms import MultiEmailField


class EmailForm(forms.Form):
    sender = forms.EmailField()
    subject = forms.CharField(max_length=128)
    receivers = MultiEmailField()
    cc = MultiEmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)
