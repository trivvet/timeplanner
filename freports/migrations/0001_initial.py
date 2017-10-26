# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=256, verbose_name='\u041f\u0440\u0456\u0437\u0432\u0438\u0449\u0435')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name="\u0406\u043c'\u044f \u0442\u0430 \u043f\u043e-\u0431\u0430\u0442\u044c\u043a\u043e\u0432\u0456")),
                ('status', models.CharField(max_length=256, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0443\u0447\u0430\u0441\u043d\u0438\u043a\u0430')),
                ('address', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441\u0430 \u0443\u0447\u0430\u0441\u043d\u0438\u043a\u0430')),
                ('phone', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u0443\u0447\u0430\u0441\u043d\u0438\u043a\u0430')),
                ('info', models.TextField(blank=True, verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0442\u0430\u043a\u0442',
                'verbose_name_plural': '\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u0438',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('number_year', models.CharField(max_length=128, null=True)),
                ('address', models.CharField(max_length=128)),
                ('plaintiff', models.CharField(max_length=128)),
                ('defendant', models.CharField(max_length=128)),
                ('object_name', models.CharField(max_length=128)),
                ('research_kind', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=True)),
                ('date_arrived', models.DateField(default=django.utils.timezone.now)),
                ('executed', models.BooleanField(default=False)),
                ('date_executed', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0434\u0456\u0457')),
                ('name', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u043f\u043e\u0434\u0456\u0457')),
                ('info', models.TextField(blank=True, verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f')),
                ('activate', models.NullBooleanField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freports.Report', verbose_name='\u0412\u0438\u0441\u043d\u043e\u0432\u043e\u043a')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u0434\u0456\u044f \u043f\u0440\u043e\u0432\u0430\u0434\u0436\u0435\u043d\u043d\u044f',
                'verbose_name_plural': '\u041f\u043e\u0434\u0456\u0457 \u043f\u0440\u043e\u0432\u0430\u0434\u0436\u0435\u043d\u043d\u044f',
            },
        ),
        migrations.CreateModel(
            name='ReportParticipants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=256, verbose_name='\u041f\u0440\u0456\u0437\u0432\u0438\u0449\u0435')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name="\u0406\u043c'\u044f \u0442\u0430 \u043f\u043e-\u0431\u0430\u0442\u044c\u043a\u043e\u0432\u0456")),
                ('status', models.CharField(max_length=256, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0443\u0447\u0430\u0441\u043d\u0438\u043a\u0430')),
                ('address', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441\u0430 \u0443\u0447\u0430\u0441\u043d\u0438\u043a\u0430')),
                ('phone', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u0443\u0447\u0430\u0441\u043d\u0438\u043a\u0430')),
                ('info', models.TextField(blank=True, verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0430 \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u044f')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freports.Report', verbose_name='\u0412\u0438\u0441\u043d\u043e\u0432\u043e\u043a')),
            ],
            options={
                'verbose_name': '\u0423\u0447\u0430\u0441\u043d\u0438\u043a \u043f\u0440\u043e\u0432\u0430\u0434\u0436\u0435\u043d\u043d\u044f',
                'verbose_name_plural': '\u0423\u0447\u0430\u0441\u043d\u0438\u043a\u0438 \u043f\u0440\u043e\u0432\u0430\u0434\u0436\u0435\u043d\u043d\u044f',
            },
        ),
    ]
