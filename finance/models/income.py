# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Income(models.Model):
    class Meta(object):
        verbose_name=u"Надходження"
        verbose_name_plural=u"Надходження"

    order = models.ForeignKey(
        "Order",
        verbose_name=u"Замовлення",
        blank=False,
        null=False,
        on_delete=models.PROTECT)

    date = models.DateField(
        verbose_name=u"Дата отримання",
        blank=False,
        null=False,
        default=timezone.now)

    account = models.ForeignKey(
        "Account",
        verbose_name=u"Цільовий рахунок",
        blank=False,
        null=False,
        on_delete=models.PROTECT)

    amount = models.IntegerField(
        verbose_name=u"Сума",
        blank=False,
        null=False,
        validators=[MinValueValidator(100),])

    payer = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Платник")

    def __str__(self):
        return u"Надходження стосовно замовлення {} на {}".format(
            self.order.name, self.account)

    def model_name(self):
        return u'Надходження'