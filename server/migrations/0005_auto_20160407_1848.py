# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_remove_userprofile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitems',
            old_name='order',
            new_name='seat',
        ),
    ]
