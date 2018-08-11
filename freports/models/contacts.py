# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Contacts(models.Model):

    class Meta(object):
        verbose_name=u"Контакт"
        verbose_name_plural=u"Контакти"

    surname = models.CharField(
        verbose_name = u"Прізвище",
        max_length=256,
        blank=False,
        null=False)

    name = models.CharField(
        verbose_name = u"Ім'я та по-батькові",
        max_length=256,
        blank=True,
        null=True)

    status = models.CharField(
        verbose_name = u"Статус в провадженні",
        max_length=256,
        blank=False,
        null=False)

    address = models.CharField(
        verbose_name = u"Адреса",
        max_length=256,
        blank=True,
        null=True)

    phone = models.CharField(
        verbose_name = u"Телефон",
        max_length=256,
        blank=True,
        null=True)

    info = models.TextField(
        blank=True,
        verbose_name=u"Додаткова інформація")

    def __unicode__(self):
        if self.name:
            return u"%s %s" % (self.surname, self.name, self.status)
        else:
            return u"%s %s" % (self.surname, self.status)
