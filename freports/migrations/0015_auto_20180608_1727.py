# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-08 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0014_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='detail',
            field=models.TextField(verbose_name='\u0414\u0435\u0442\u0430\u043b\u0456'),
        ),
    ]