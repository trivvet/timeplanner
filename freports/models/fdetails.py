# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

status_list = {
    'judge': u'Суддя',
    'plaintiff': u'Позивач',
    'defendant': u'Відповідач',
    'plaintiff_agent': u'Представник позивача',
    'defendant_agent': u'Представник відповідача',
    'other_participant': u'Інший учасник'
}

way_forward_list = {
    'post': u'поштою',
    'personally': u'особисто в приміщенні суду',
    'courier': u"від кур'єра"
}

class ReportEvents(models.Model):

    class Meta(object):
        verbose_name=u"Подія провадження"
        verbose_name_plural=u"Події провадження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False,
        on_delete=models.CASCADE)

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

    activate = models.BooleanField(
        blank=True,
        null=True)

    received = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Отримані матеріали")

    way_forward = models.CharField(
        verbose_name = u"Спосіб пересилання",
        max_length=256,
        blank=True,
        null=True
    )

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
        blank=True,
        null=True)

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

    def __str__(self):
        return u"Report %s: %s" % (self.report.number, self.name)

    def detail_info(self):
        description = ""
        if self.name == 'first_arrived':
            if self.received:
                description = 'Надійшла ухвала суду від {} року. Разом з ухвалою надійшли: {}'.format(self.decision_date.strftime('%d-%m-%Y'), self.received)
            else:
                description = 'Надійшла ухвала суду від %s року без додаткових матеріалів' % self.decision_date.strftime('%d-%m-%Y')
            if self.way_forward:
                description += ". Отримано {}".format(way_forward_list[self.way_forward])
        elif self.name == 'arrived':
            description = 'Надійшли матеріали: %s' % self.received
            description += ". Отримано {}".format(way_forward_list[self.way_forward])
        elif self.name == 'petition':
            if self.sending:
                description = 'Направлено клопотання %s, а саме: %s. Разом з клопотанням повернено: %s' % (self.subspecies, self.necessary, self.sending)
            else:
                description = 'Направлено клопотання %s, а саме: %s' % (self.subspecies, self.necessary)
        elif self.name == 'bill':
            if self.address:
                description = '%s на адресу %s на суму %s грн' % (self.subspecies, self.address, self.cost)
            elif self.subspecies:
                description = '%s на суму %s грн' % (self.subspecies, self.cost)
            else:
                description = 'На суму {} грн'.format(self.cost)
        elif self.name == 'paid':
            description = self.subspecies
        elif self.name == 'schedule':
            pz = timezone.get_current_timezone()
            self.time = pz.normalize(self.time)
            time_info = self.time.strftime('%H:%M')
            date_info = self.time.strftime('%d-%m-%Y')
            inspect_info = 'Призначено виїзд о %s на %s' % (time_info, date_info)
            description = 'Тип повідомлення: {}. {}'.format(self.subspecies, inspect_info)
        elif self.name == 'inspected':
            description = self.subspecies
        elif self.name == 'done':
            description = 'Направлено %s. Додатки: %s' % (self.subspecies, self.sending)

        return description + '. ' + self.info

    def short_info(self):
        descriptions = {
            'first_arrived': u"Надійшла ухвала",
            'arrived': u"Надійшли матеріали",
            'petition': u"Направлене клопотання",
            'bill': u"Направлений рахунок",
            'paid': u"Проведена оплата",
            'schedule': u"Призначено виїзд",
            'inspected': u"Проведено огляд",
            'done': u"Зданий до суду"
        }
        return descriptions[self.name]

class ReportParticipants(models.Model):

    class Meta(object):
        verbose_name=u"Учасник провадження"
        verbose_name_plural=u"Учасники провадження"

    report = models.ForeignKey('Report',
        verbose_name=u"Висновок",
        blank=False,
        null=False,
        on_delete=models.PROTECT)

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

    def __str__(self):
        return u"%s %s (report %s/%s)" % (self.status, self.surname, self.report.number, self.report.number_year)

    def full_info(self):
        return u"{} {} ({})".format(
            self.surname, self.name, status_list[self.status])

    def full_name(self):
        return u"{} {}".format(
            self.surname, self.name)

    @property
    def status_name(self):
        status_list = {
            'judge': 'Суддя',
            'plaintiff': 'Позивач',
            'defendant': 'Відповідач',
            'plaintiff_agent': 'Представник позивача',
            'defendant_agent': 'Представник відповідача',
            'other_participant': 'Інший учасник'
        }
        return status_list[self.status]
    






