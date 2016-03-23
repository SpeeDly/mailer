from django.db import models
from django.contrib.auth.models import User

from mailer.utils.models import EmailListField


class Email(models.Model):
    user = models.ForeignKey(User, related_name="profile")
    sender = models.EmailField(max_length=128, blank=False, null=False)
    recipients = EmailListField(max_length=128, blank=False, null=False)
    subject = EmailListField(max_length=128, blank=True, null=True)
    cc = EmailListField(max_length=128, blank=True, null=True)
    message = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)

