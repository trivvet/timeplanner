from __future__ import unicode_literals

from django.db import models

from .income import Income
from .execution import Execution


class Account(models.Model):
    STATUS_VARIANT = (
        ('self', u'Особистий'),
        ('work', u'Робочий'),
    )

    class Meta(object):
        verbose_name=u"Рахунок"
        verbose_name_plural=u"Рахунки"

    title = models.CharField(
        verbose_name=u"Назва рахунку",
        max_length=256,
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

    def __str__(self):
        return u"Рахунок {} ({})".format(
            self.title, dict(self.STATUS_VARIANT)[self.status])

    def remainder(self):
        account = self
        incomes = Income.objects.filter(account=account)
        executions = Execution.objects.filter(account=account)
        total_sum = 0
        for income in incomes:
            total_sum += income.amount
        for execution in executions:
            total_sum -= execution.amount
        return total_sum

