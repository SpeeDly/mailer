# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 13:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_auto_20160322_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 3, 23, 13, 38, 0, 897550, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
