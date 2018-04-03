# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-03 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0012_task2'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='freports.ReportEvents', verbose_name='\u041f\u043e\u0434\u0456\u044f'),
        ),
        migrations.AlterField(
            model_name='task',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='freports.Report', verbose_name='\u041f\u0440\u043e\u0432\u0430\u0434\u0436\u0435\u043d\u043d\u044f'),
        ),
    ]
