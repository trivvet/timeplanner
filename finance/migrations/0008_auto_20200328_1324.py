# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-03-28 11:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_remove_account_total_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AlterField(
            model_name='execution',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100)], verbose_name='\u0421\u0443\u043c\u0430 \u0437\u0430\u043a\u0440\u0438\u0442\u0442\u044f'),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100)], verbose_name='\u0421\u0443\u043c\u0430'),
        ),
    ]
