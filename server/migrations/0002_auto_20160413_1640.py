# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='table',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
    ]
