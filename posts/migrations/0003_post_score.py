# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-30 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20161029_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
