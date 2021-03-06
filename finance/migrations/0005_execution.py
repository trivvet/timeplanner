# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-29 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0432\u0438\u043a\u043e\u043d\u0430\u043d\u043d\u044f')),
                ('amount', models.IntegerField(verbose_name='\u0421\u0443\u043c\u0430 \u0437\u0430\u043a\u0440\u0438\u0442\u0442\u044f')),
                ('closed_tasks', models.CharField(blank=True, max_length=256, null=True, verbose_name='\u0417\u0430\u043a\u0440\u0438\u0442\u0456 \u0442\u0430\u0441\u043a\u0438')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Account', verbose_name='\u0426\u0456\u043b\u044c\u043e\u0432\u0438\u0439 \u0440\u0430\u0445\u0443\u043d\u043e\u043a')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Order', verbose_name='\u0417\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f')),
            ],
            options={
                'verbose_name': '\u0412\u0438\u043a\u043e\u043d\u0430\u043d\u043d\u044f',
                'verbose_name_plural': '\u0412\u0438\u043a\u043e\u043d\u0430\u043d\u043d\u044f',
            },
        ),
    ]
