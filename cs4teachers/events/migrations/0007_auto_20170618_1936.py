# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 07:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20170618_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
