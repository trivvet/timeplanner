# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-23 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0010_auto_20171223_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='waiting_days',
            new_name='waiting_days_amount',
        ),
        migrations.AddField(
            model_name='report',
            name='active_days_amount',
            field=models.IntegerField(default=0),
        ),
    ]