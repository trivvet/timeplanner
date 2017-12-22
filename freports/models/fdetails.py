# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class ReportEvents(models.Model):

    class Meta(object):
        verbose_name=u"Подія провадження"
        verbose_name_plural=u"Події провадження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False)

    date = models.DateField(
        verbose_name = u"Дата події",
        blank=False,
        default=timezone.now)

    name = models.CharField(
        verbose_name = u"Назва події",
        max_length=256,
        blank=False,
        null=False)

    info = models.TextField(
        blank=True,
        verbose_name=u"Додаткова інформація")

    activate = models.NullBooleanField(
        blank=True,
        null=True)

    received = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Отримані матеріали")

    decision_date = models.DateField(
        verbose_name = u"Дата ухвали",
        blank=True,
        null=True)

    time = models.DateTimeField(
        verbose_name = u"Дата та час огляду",
        blank=True,
        null=True)

    subspecies = models.CharField(
        verbose_name = u"Підвид події",
        max_length=256,
        blank=True)

    necessary = models.TextField(
        blank=True,
        verbose_name=u"Зміст клопотання")

    address = models.TextField(
        blank=True,
        verbose_name=u"Адреса направлення")

    cost = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u"Вартість висновку")

    sending = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Направлені матеріали")

    def __unicode__(self):
        return u"Report %s: %s" % (self.report.number, self.name)

    def detail_info(self):
        description = ""
        if self.name == 'first_arrived':
            if self.received:
                description = 'Надійшла ухвала суду від %s року. Разом з ухвалою надійшли: %s' % (self.decision_date.strftime('%d-%m-%Y'), self.received)
            else:
                description = 'Надійшла ухвала суду від %s року без додаткових матеріалів' % self.decision_date.strftime('%d-%m-%Y')
        elif self.name == 'arrived':
            description = 'Надійшли матеріали: %s' % self.received
        elif self.name == 'petition':
            if self.sending:
                description = 'Направлено клопотання %s, а саме: %s. Разом з клопотанням повернено: %s' % (self.subspecies, self.necessary, self.sending)
            else:
                description = 'Направлено клопотання %s, а саме: %s' % (self.subspecies, self.necessary)
        elif self.name == 'bill':
            if self.address:
                description = '%s на адресу %s на суму %s грн' % (self.subspecies, self.address, self.cost)
            else:
                description = '%s на суму %s грн' % (self.subspecies, self.cost)
        elif self.name == 'paid':
            description = self.subspecies
        elif self.name == 'schedule':
            description = 'Призначено виїзд о %s на %s' % (self.time.strftime('%H:%M'), self.time.strftime('%d-%m-%Y'))
        elif self.name == 'inspected':
            description = self.subspecies
        elif self.name == 'done':
            description = 'Направлено %s. Додатки: %s' % (self.subspecies, self.sending)

        return description + '. ' + self.info

class ReportParticipants(models.Model):

    class Meta(object):
        verbose_name=u"Учасник провадження"
        verbose_name_plural=u"Учасники провадження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False)

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
        verbose_name = u"Статус учасника",
        max_length=256,
        blank=False,
        null=False)

    address = models.CharField(
        verbose_name = u"Адреса учасника",
        max_length=256,
        blank=True,
        null=True)

    phone = models.CharField(
        verbose_name = u"Телефон учасника",
        max_length=256,
        blank=True,
        null=True)

    info = models.TextField(
        blank=True,
        verbose_name=u"Додаткова інформація")

    def __unicode__(self):
        return u"%s %s (report %s/%s)" % (self.status, self.surname, self.report.number, self.report.number_year)

class ReportDaysInfo(models.Model):

    class Meta(object):
        verbose_name=u"Дні у виконанні"
        verbose_name_plural=u"Дні у виконанні"

    report = models.ForeignKey('Report',
        verbose_name=u'Висновок',
        blank=False,
        null=False)

    change_date = models.DateField(
        blank=False,
        default=timezone.now)

    active_days = models.IntegerField(
        blank=True,
        null=True)

    waiting_days = models.IntegerField(
        blank=True,
        null=True)

    def __unicode__(self):
        return u"Amount days for report %s" % (self.report)
