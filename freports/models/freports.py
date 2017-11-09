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
        return u"%s/017-%s-%s" % (self.number, self.address, self.plaintiff)
