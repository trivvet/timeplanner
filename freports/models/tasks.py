# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Task(models.Model):
    class Meta(object):
        verbose_name=u"Завдання"
        verbose_name_plural=u"Завдання"

    report = models.ForeignKey('Report',
        verbose_name=u"Провадження",
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    event = models.ForeignKey('ReportEvents',
        verbose_name=u"Подія",
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    time = models.DateTimeField(
        verbose_name=u"Дата та час завдання",
        blank=False,
        default=timezone.now)

    execute = models.BooleanField(
        verbose_name=u"Статус виконання",
        blank=True,
        null=True)

    kind = models.CharField(
        verbose_name = u"Вид завдання",
        max_length=256,
        blank=False,
        null=False)

    detail = models.TextField(
        blank=False,
        null=False,
        verbose_name=u"Деталі")

    def __str__(self):
        return u"%s %s" % (self.kind, self.time.strftime("%H-%M %d-%m-%Y"))