# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-18 00:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20160420_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
