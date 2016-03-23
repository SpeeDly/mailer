# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import mailer.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', mailer.utils.models.EmailListField(max_length=128)),
                ('sender', models.EmailField(max_length=128)),
                ('subject', mailer.utils.models.EmailListField(blank=True, max_length=128, null=True)),
                ('cc', mailer.utils.models.EmailListField(blank=True, max_length=128, null=True)),
                ('bcc', mailer.utils.models.EmailListField(blank=True, max_length=128, null=True)),
                ('message', models.TextField(null=True)),
            ],
        ),
    ]