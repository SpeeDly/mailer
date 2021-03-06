from django.db import models

from mailer.utils.models import EmailListField


class Email(models.Model):
    sender = models.EmailField(max_length=128, blank=False, null=False)
    receivers = EmailListField(max_length=128, blank=False, null=False)
    subject = models.CharField(max_length=128, blank=True, null=True)
    cc = EmailListField(max_length=128, blank=True, null=True)
    message = models.TextField(null=True)


class Status(models.Model):
    provider = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    response = models.TextField()


class EmailStatus(models.Model):
    email = models.ForeignKey(Email)
    status = models.ForeignKey(Status)
