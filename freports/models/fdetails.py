# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class ReportEvents(models.Model):

    class Meta(object):
        verbose_name=u"Подія провадження"
        verbose_name_plural=u"Події провадження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False)

    date = models.DateField(
        verbose_name = u"Дата події",
        blank=False,
        default=timezone.now)

    name = models.CharField(
        verbose_name = u"Назва події",
        max_length=256,
        blank=False,
        null=False)

    info = models.TextField(
        blank=True,
        verbose_name=u"Додаткова інформація")

    activate = models.NullBooleanField(
        blank=True,
        null=True)

    def __unicode__(self):
        return u"Report %s: %s" % (self.report.number, self.info)

class ReportParticipants(models.Model):

    class Meta(object):
        verbose_name=u"Учасник провадження"
        verbose_name_plural=u"Учасники провадження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False)

    surname = models.CharField(
        verbose_name = u"Прізвище",
        max_length=256,
        blank=False,
        null=False)

    name = models.CharField(
        verbose_name = u"Ім'я та по-батькові",
        max_length=256,
        blank=True,
        null=True)

    status = models.CharField(
        verbose_name = u"Статус учасника",
        max_length=256,
        blank=False,
        null=False)

    address = models.CharField(
        verbose_name = u"Адреса учасника",
        max_length=256,
        blank=True,
        null=True)

    phone = models.CharField(
        verbose_name = u"Телефон учасника",
        max_length=256,
        blank=True,
        null=True)

    info = models.TextField(
        blank=True,
        verbose_name=u"Додаткова інформація")

    def __unicode__(self):
        return u"%s %s (report %s/%s)" % (self.status, self.surname, self.report.number, self.report.number_year)
