# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0003_forensicreport_data_arrived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forensicreport',
            name='data_arrived',
        ),
        migrations.AddField(
            model_name='forensicreport',
            name='date_arrived',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
