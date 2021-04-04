# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.utils import timezone

from .fdetails import ReportEvents
from finance.models import Order

# Create your models here.

class BaseReport(models.Model):
    number = models.IntegerField(
        blank=False,
        null=False)

    number_year = models.CharField(
        max_length=128,
        blank=False,
        null=True)

    address = models.CharField(
        verbose_name=u"Адреса",
        max_length=128,
        blank=False,
        null=False)

    object_name = models.CharField(
        verbose_name=u"Назва об'єкта",
        max_length=128,
        blank=False,
        null=False)

    research_kind = models.CharField(
        verbose_name=u"Вид дослідження",
        max_length=128,
        blank=False,
        null=False)

    active = models.BooleanField(
        verbose_name=u"Активний статус",
        null=True,
        blank=False)

    cost = models.IntegerField(
        blank=True,
        null=True)

    date_arrived = models.DateField(
        blank=False,
        default=timezone.now)

    executed = models.BooleanField(
        blank=False,
        default=False)

    date_executed = models.DateField(
        blank=True,
        null=True)

    change_date = models.DateField(
        blank=False,
        default=timezone.now)

    active_days_amount = models.IntegerField(
        blank=False,
        default=0)

    class Meta:
        abstract = True


class Report(BaseReport):
    case_number = models.CharField(
        max_length=128,
        blank=True,
        null=True)

    repeater_report = models.BooleanField(
        verbose_name=u"Повторна експертиза",
        null=True,
        blank=True
    )

    additional_report = models.BooleanField(
        verbose_name=u"Додаткова експертиза",
        null=True,
        blank=True
    )

    judge_name = models.ForeignKey('Judge',
        verbose_name=u"Суддя",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    plaintiff = models.CharField(
        max_length=128,
        blank=False,
        null=False)

    defendant = models.CharField(
        max_length=128,
        blank=False,
        null=False)

    waiting_days_amount = models.IntegerField(
        blank=True,
        null=True)

    def __str__(self):
        return u"{number}/{number_year} ({address}-{plaintiff}-{defendant})".format(number=self.number,
            number_year=self.number_year, address=self.address, plaintiff=self.plaintiff, defendant=self.defendant)

    def clean(self):
         if self.repeater_report and self.additional_report():
             raise ValidationError("Both fields can't be choosed")

    def filled_info(self):
        if self.address == '-' or self.judge_name == '-' or self.plaintiff == '-' or self.defendant == '-' or self.object_name == '-' or self.research_kind == '-':
            answer = False
        else:
            answer = True
        return answer

    def short_name(self):
        return u"{number}/{number_year}-{address}-{plaintiff}-{defendant}-{object_name}-{research_kind}".format(
            number=self.number, number_year=self.number_year, address=self.address, plaintiff=self.plaintiff,
            defendant=self.defendant, object_name=self.object_name, research_kind=self.research_kind)

    def full_number(self):
        if self.repeater_report:
            add_letter = u'п'
        elif self.additional_report:
            add_letter = u'д'
        else:
            add_letter = ''
        return u"{}{}/{}".format(self.number, add_letter, self.number_year)

    def time_after_update(self):
        time_amount = date.today() - self.change_date
        return time_amount.days

    def is_paid(self):
        paid = ReportEvents.objects.filter(report=self, name='paid')
        return paid.exists()

    def is_cost(self):
        cost = self.cost
        if not self.cost:
            bill = ReportEvents.objects.filter(report=self, name='bill')
            if bill.exists():
                cost = bill.first().cost
        return cost

    @property
    def final_document(self):
        events = ReportEvents.objects.filter(report=self).order_by('date', 'id')
        if events.count() != 0:
            report_type = events.last()
        else:
            report_type = ''
        return report_type

    @property
    def short_info(self):
        return u"{address}-{plaintiff}-{defendant}".format(address=self.address, 
            plaintiff=self.plaintiff, defendant=self.defendant)

    @property
    def order(self):
        orders_list = Order.objects.filter(report=self)
        if orders_list:
            order = orders_list[0]
        else:
            order = None
        return order


class Research(BaseReport):
    applicant = models.CharField(
        verbose_name=u"Замовник",
        max_length=128,
        blank=False,
        null=False)

    addition_info = models.TextField(
        blank=True,
        verbose_name=u"Додаткова інформація")

    def __str__(self):
        return u"Дослідження {number}ед/{number_year} ({applicant})".format(
            number=self.number, number_year=self.number_year, 
            address=self.address, applicant=self.applicant)

    def filled_info(self):
        if self.address == '-' or self.applicant == '-' or self.object_name == '-' or self.research_kind == '-':
            answer = False
        else:
            answer = True
        return answer

    def short_name(self):
        return u"{number}/{number_year}-{address}-{applicant}-{object_name}-{research_kind}".format(
            number=self.number, number_year=self.number_year, 
            address=self.address, plaintiff=self.applicant,
            object_name=self.object_name, research_kind=self.research_kind)

    def full_number(self):
        return u"{}ед/{}".format(self.number, self.number_year)

    def time_after_update(self):
        time_amount = date.today() - self.change_date
        return time_amount.days