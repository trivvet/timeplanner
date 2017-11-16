# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

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
        blank=True)

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
        return u"%s/017-%s-%s" % (self.number, self.address, self.plaintiff)

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
