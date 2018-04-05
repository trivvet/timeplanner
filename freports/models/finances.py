# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Account(models.Model):
    class Meta(object):
        verbose_name=u"Рахунок"
        verbose_name_plural=u"Рахунки"

    title = models.CharField(
        verbose_name = u"Назва рахунку",
        max_length=256,
        blank=False,
        null=False)

    total_sum = models.IntegerField(
        verbose_name=u"Сума на рахунку",
        blank=False,
        null=False)

    cash = models.BooleanField(
        verbose_name=u"Готівка",
        blank=False,
        null=False)

    status = models.CharField(
        verbose_name = u"Статус рахунку",
        max_length=256,
        choices = (("self", u"Особистий"), ("work", u"Робочий")),
        blank=False,
        null=False)

    credit_cash = models.IntegerField(
        verbose_name=u"Кошти в кредитах",
        blank=True,
        null=True)

    def __unicode__(self):
        return u"Рахунок {} ({})".format(self.title, self.status)