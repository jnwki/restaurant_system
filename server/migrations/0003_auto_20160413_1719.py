# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20160413_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditem',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]