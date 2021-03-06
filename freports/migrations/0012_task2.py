# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-14 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0011_auto_20171223_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0442\u0430 \u0447\u0430\u0441 \u0437\u0430\u0432\u0434\u0430\u043d\u043d\u044f')),
                ('kind', models.CharField(max_length=256, verbose_name='\u0412\u0438\u0434 \u0437\u0430\u0432\u0434\u0430\u043d\u043d\u044f')),
                ('detail', models.CharField(max_length=256, verbose_name='\u0414\u0435\u0442\u0430\u043b\u0456')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='freports.ReportEvents', verbose_name='\u041f\u043e\u0434\u0456\u044f')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u0432\u0434\u0430\u043d\u043d\u044f',
                'verbose_name_plural': '\u0417\u0430\u0432\u0434\u0430\u043d\u043d\u044f',
            },
        ),
    ]
