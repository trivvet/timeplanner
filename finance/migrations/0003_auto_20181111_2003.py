# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-11 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid_sum',
            field=models.IntegerField(default=0, verbose_name='\u041e\u043f\u043b\u0430\u0447\u0435\u043d\u0430 \u0441\u0443\u043c\u0430'),
        ),
    ]