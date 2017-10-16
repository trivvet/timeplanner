# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class ReportDetails(models.Model):

    class Meta(object):
        verbose_name=u"Детальна інформація"
        verbose_name_plural=u"Детальна інформація"

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

    def __unicode__(self):
        return u"Report %s: %s" % (self.report.number, self.info)
