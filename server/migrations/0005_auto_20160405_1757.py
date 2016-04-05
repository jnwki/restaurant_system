# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_order_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='order',
            name='seat_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='table_number',
            field=models.IntegerField(default=1),
        ),
    ]
