# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-23 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0009_auto_20171223_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='change_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
