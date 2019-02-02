# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.utils import timezone

from .fdetails import ReportEvents

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

    active = models.NullBooleanField(
        verbose_name=u"Активний статус",
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

    judge_name = models.ForeignKey('Judge',
        verbose_name=u"Суддя",
        blank=True,
        null=True)

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

    def __unicode__(self):
        return u"{number}/{number_year} ({address}-{plaintiff}-{defendant})".format(number=self.number,
            number_year=self.number_year, address=self.address, plaintiff=self.plaintiff, defendant=self.defendant)

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
        return u"{}/{}".format(self.number, self.number_year)

    def time_after_update(self):
        time_amount = date.today() - self.change_date
        return time_amount.days


class Research(BaseReport):
    applicant = models.CharField(
        verbose_name=u"Замовник",
        max_length=128,
        blank=False,
        null=False)

    addition_info = models.TextField(
        blank=True,
        max_length=256,
        verbose_name=u"Додаткова інформація")

    def __unicode__(self):
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