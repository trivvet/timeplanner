# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Order(models.Model):
    STATUS_VARIANT = (
        ('active', u'Активне'),
        ('inactive', u'Призупинене'),
        ('done', u'Виконане'),
    )

    class Meta(object):
        verbose_name=u"Замовлення"
        verbose_name_plural=u"Замовлення"

    name = models.CharField(
        verbose_name=u"Назва замовлення",
        max_length=256,
        blank=False,
        null=False)

    report = models.ForeignKey('freports.Report',
        verbose_name=u"Провадження",
        blank=True,
        null=True)

    total_sum = models.IntegerField(
        verbose_name=u"Кошторисна вартість",
        blank=False,
        null=False)

    paid_sum = models.IntegerField(
        verbose_name=u"Оплачена сума",
        blank=False,
        null=False,
        default=0)

    done_sum = models.IntegerField(
        verbose_name=u"Вартість виконаних робіт",
        blank=False,
        null=False,
        default=0)

    tasks_number = models.IntegerField(
        verbose_name=u"Кількість необхідних тасків",
        blank=True,
        null=True)

    status = models.CharField(
        verbose_name=u"Статус виконання",
        max_length=256,
        blank=False,
        null=False,
        choices=STATUS_VARIANT)

    def __unicode__(self):
        if self.report:
            return u"Замовлення {} ({})".format(
                self.name, self.report)
        else:
            return u"Замовлення {}".format(self.name)