# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Execution(models.Model):
    class Meta(object):
        verbose_name=u"Виконання"
        verbose_name_plural=u"Виконання"

    order = models.ForeignKey(
        "Order",
        verbose_name=u"Замовлення",
        blank=False,
        null=False)

    date = models.DateField(
        verbose_name=u"Дата виконання",
        blank=False,
        null=False,
        default=timezone.now)

    account = models.ForeignKey(
        "Account",
        verbose_name=u"Цільовий рахунок",
        blank=False,
        null=False)

    amount = models.IntegerField(
        verbose_name=u"Сума закриття",
        blank=False,
        null=False)

    closed_tasks = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Закриті таски")

    def __unicode__(self):
        return u"Виконання {}".format(
            self.order)

    def model_name(self):
        return 'Виконання'