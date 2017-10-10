# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ForensicReport(models.Model):
    number = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )

    address = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )

    plaintiff = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )

    defendant = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )

    object_name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )

    research_kind = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )
