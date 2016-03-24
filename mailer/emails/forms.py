from django import forms

from mailer.utils.forms import MultiEmailField
from mailer.emails.models import Email


class EmailForm(forms.Form):
    sender = forms.EmailField()
    subject = forms.CharField(max_length=128, required=False)
    receivers = MultiEmailField()
    cc = MultiEmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        email = Email.objects.create(**data)
        return email
