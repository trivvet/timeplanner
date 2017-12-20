# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.utils import timezone

from .fdetails import ReportEvents

# Create your models here.

class Report(models.Model):
    number = models.IntegerField(
        blank=False,
        null=False)

    number_year = models.CharField(
        max_length=128,
        blank=False,
        null=True)

    case_number = models.CharField(
        max_length=128,
        blank=True,
        null=True)

    address = models.CharField(
        max_length=128,
        blank=False,
        null=False)

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

    object_name = models.CharField(
        max_length=128,
        blank=False,
        null=False)

    research_kind = models.CharField(
        max_length=128,
        blank=False,
        null=False)

    active = models.BooleanField(
        blank=False,
        default=True)

    date_arrived = models.DateField(
        blank=False,
        default=timezone.now)

    executed = models.BooleanField(
        blank=False,
        default=False)

    date_executed = models.DateField(
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

    def active_days(self):
        details = ReportEvents.objects.filter(report=self).order_by('date')
        days_amount = 0
        last_event = details.reverse()[0]
        if details.count() > 0:
            before_detail = details[0]
            for detail in details:
                if detail.activate == False and before_detail.activate == True:
                    time = detail.date - before_detail.date
                    days_amount += time.days
                if detail.activate is not None:
                    before_detail = detail

        try:
            time = self.date_executed - last_event.date
            days_amount += time.days
        except TypeError:
            pass
        if details.count() == 0 or detail.activate == True:
            time = date.today() - last_event.date
            days_amount += time.days

        return days_amount
