# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.utils import timezone

from .fdetails import ReportEvents, ReportParticipants

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

    active = models.NullBooleanField(
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

    def active_days(self):
        return self.active_days_amount + self.time_after_update()

    def waiting_days(self):
        return self.waiting_days_amount + self.time_after_update()

    @property
    def events(self):
        instance = self
        qs = ReportEvents.objects.filter(report=instance)
        return qs

    @property
    def last_event(self):
        events = self.events.order_by('date')
        return events.last()

    @property
    def participants(self):
        instance = self
        qs = ReportParticipants.objects.filter(report=instance)
        return qs
    
    
    
