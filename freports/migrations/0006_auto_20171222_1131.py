# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0005_auto_20171222_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportdaysinfo',
            name='report',
        ),
        migrations.AddField(
            model_name='report',
            name='days_info',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='freports.ReportDaysInfo'),
        ),
    ]
