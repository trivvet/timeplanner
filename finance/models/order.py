# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Order(models.Model):

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
        null=True,
        on_delete=models.CASCADE)

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

    tasks_number = models.FloatField(
        verbose_name=u"Кількість необхідних тасків",
        blank=True,
        null=True)

    def __str__(self):
        if self.report:
            return u"Замовлення {} ({})".format(
                self.name, self.report)
        else:
            return u"Замовлення {}".format(self.name)

    @property
    def remainder(self):
        return self.paid_sum - self.done_sum

    @property
    def unpaid_sum(self):
        return self.total_sum - self.paid_sum
    
    