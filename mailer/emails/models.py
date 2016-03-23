from django.db import models
from mailer.utils.models import EmailListField


class Email(models.Model):
    sender = models.EmailField(max_length=128, blank=False, null=False)
    recipients = EmailListField(max_length=128, blank=False, null=False)
    subject = EmailListField(max_length=128, blank=True, null=True)
    cc = EmailListField(max_length=128, blank=True, null=True)
    message = models.TextField(null=True)

