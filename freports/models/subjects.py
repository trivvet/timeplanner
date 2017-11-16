# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ReportSubject(models.Model):

    class Meta(object):
        verbose_name=u"Об'єкт дослідження"
        verbose_name_plural=u"Об'єкти дослідження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False)

    subject_type = models.CharField(
        verbose_name = u"Вид об'єкту",
        max_length=256,
        blank=False,
        null=False)

    settlement = models.CharField(
        verbose_name = u"Населений пункт",
        max_length=256,
        blank=False,
        null=False)

    region = models.CharField(
        verbose_name = u"Район області",
        max_length=256,
        blank=True,
        null=True)

    street = models.CharField(
        verbose_name = u"Вулиця",
        max_length=256,
        blank=False,
        null=False)

    building = models.CharField(
        verbose_name = u"Номер будинку",
        max_length=256,
        blank=True,
        null=True)

    flat = models.CharField(
        verbose_name = u"Номер квартири",
        max_length=256,
        blank=True,
        null=True)

    research_type = models.CharField(
        verbose_name = u"Тип дослідження об'єкту",
        max_length=256,
        blank=False,
        null=False)

    def __unicode__(self):
        return u"Subject %s of the report %s/%s" % (self.subject_type, self.report.number, self.report.number_year)

    def short_address(self):
        if self.settlement == 'м. Хмельницький' or 'с.т.' in self.street and self.region == 'Хмельницький':
            short_address = self.street
        elif 'с.т.' in self.street:
            short_address = self.region + 'р-н'
        else:
            short_address = self.settlement
        return short_address

    def full_address(self):
        if self.settlement_name() == 'Хмельницький':
            full_address = u"м. Хмельницький, %s" % self.street
        else:
            if self.region:
                full_address = u"%s, %s, %s" % (self.region, self.settlement, self.street)
            else:
                full_address = u"%s, %s" % (self.settlement, self.street)
        if self.building:
            full_address += ', %s' % self.building
        if self.flat:
            full_address += ', кв. №%s' % self.flat

        return full_address

    def settlement_type(self):
        s_type = self.settlement[0:4]
        if '.' not in s_type:
            s_type = ''
        else:
            s_type = s_type[0:2]
        return s_type

    def settlement_name(self):
        split_name = self.settlement.split('. ')
        if len(split_name) > 1:
            name = split_name[1]
        else:
            name = self.settlement
        return name

    def street_type(self):
        s_type = self.street[0:4]
        return s_type

    def street_name(self):
        split_name = self.street.split('. ')
        if len(split_name) > 1:
            name = split_name[1]
        else:
            name = self.street
        return name
