# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Court(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name=u"Назва суду")

    number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u"Код справ")

    address = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Адреса")

    chair = models.OneToOneField('Judge',
        verbose_name=u"Голова суду",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s" % self.name


class Judge(models.Model):
    surname = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name=u"Прізвище")

    first_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name=u"Ім'я")

    second_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name=u"Ім'я по батькові")

    court_name = models.ForeignKey('Court',
        verbose_name=u"Суд",
        blank=False,
        null=False)

    personal_phone = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Особистий телефон")

    work_phone = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Робочий телефон")

    address = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=u"Домашня адреса")

    def __unicode__(self):
        return u"%s %s. %s. (%s)" %(self.surname, self.first_name[0], self.second_name[0], self.court)


