# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0004_reportdaysinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='active',
            field=models.NullBooleanField(),
        ),
    ]
