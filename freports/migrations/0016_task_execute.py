# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-13 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0015_auto_20180608_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='execute',
            field=models.NullBooleanField(verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0432\u0438\u043a\u043e\u043d\u0430\u043d\u043d\u044f'),
        ),
    ]
