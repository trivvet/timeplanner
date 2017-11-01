# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Report, ReportEvents, ReportParticipants

petition_type = ['Про надання додаткових матеріалів', 'Про уточнення питань', 'Про надання справи']
done_type = ['Висновок експерта', 'Повідомлення про неможливість', 'Залишення без виконання']
inspected_type = ['Проведено успішно', 'Не надано доступ', 'Відмінено']
bill_type = ['Направлено рекомендованого листа', 'Вручено особисто', 'Вручено представнику', 'Направлено електронного листа']
paid_type = ['На банківський рахунок', 'Готівкою']
kind_specific = {
        'first_arrived': ['надходження ухвали про призначення експертизи', ['date', 'info', 'received', 'decision_date']],
        'arrived': ['надходження з суду', ['date', 'info', 'received']],
        'petition': ['направлення клопотання', ['date', 'info', 'type', 'necessary', 'sending'], petition_type],
        'bill': ['направлення рахунку', ['date', 'info', 'cost', 'address', 'type'], bill_type],
        'paid': ['оплата', ['date', 'info', 'type'], paid_type],
        'schedule': ['призначення виїзду', ['date', 'info', 'time']],
        'inspected': ['проведення огляду', ['date', 'info', 'type'], inspected_type],
        'done': ['відправлення до суду', ['date', 'info', 'sending', 'type'], done_type]}

@login_required(login_url='/login/')
def details_list(request, rid):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(report=Report.objects.get(pk=rid)).order_by('date')
    participants = ReportParticipants.objects.filter(report=Report.objects.get(pk=rid))

    return render(request, 'freports/report_detail.html', {'details': details, 'report': report, 'participants': participants})

@login_required(login_url='/login/')
def add_detail(request, rid, kind):
    report = Report.objects.get(pk=rid)
    content = {}
    header = {}
    header['main'] = u'Додавання події до провадження №%s/%s' % (report.number, report.number_year)
    header['second'] = kind_specific[kind][0].capitalize()
    content['obvious_fields'] = kind_specific[kind][1]
    if 'type' in content['obvious_fields']:
        content['select_type'] = kind_specific[kind][2]
    content['kind'] = kind

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html',
                    {'header': header, 'content': content, 'new_content': new_element, 'errors': errors})

            else:
                if new_element['activate'] == 'executed':
                    new_element['activate'] = False
                    report.executed = True
                    report.date_executed = new_element['date']
                    report.save()
                new_detail = ReportEvents(**new_element)
                new_detail.save()
                last_detail = ReportEvents.objects.filter(report=report).order_by('date').reverse()[0]
                if last_detail.activate == True:
                    report.active = True
                    report.save()
                elif last_detail.activate == False:
                    report.active = False
                    report.save()
                messages.success(request, u"Подія '%s' успішно додана" % new_detail.name)

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання деталей провадження скасовано")

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        return render(request, 'freports/detail_form.html', {'header': header, 'content': content})

@login_required(login_url='/login/')
def edit_detail(request, rid, did):
    report = Report.objects.get(pk=rid)
    detail = ReportEvents.objects.get(pk=did)
    content = {}
    header = {}
    header['main'] = u'Редагування події провадження №%s/%s' % (report.number, report.number_year)
    header['second'] = kind_specific[detail.name][0].capitalize()
    content['obvious_fields'] = kind_specific[detail.name][1]
    if 'type' in content['obvious_fields']:
        content['select_type'] = kind_specific[detail.name][2]
    content['kind'] = detail.name

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_data = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html',
                    {'header': header, 'content': content, 'new_content': new_data, 'errors': errors})

            else:
                edit_detail = ReportEvents(**new_data)
                edit_detail.id = did
                if new_data['activate'] == 'executed':
                    edit_detail.activate = False
                    report.executed = True
                    report.date_executed = new_data['date']
                    report.save()
                else:
                    edit_detail.activate = new_data['activate']
                edit_detail.save()
                last_detail = ReportEvents.objects.filter(report=report).order_by('date').reverse()[0]
                if last_detail.activate == True:
                    report.active = True
                    report.save()
                elif last_detail.activate == False:
                    report.active = False
                    report.save()
                messages.success(request, u"Подія '%s' успішно змінена" % edit_detail.name)

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування деталей провадження скасовано")

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        new_content = detail
        new_content.date = new_content.date.isoformat()
        return render(request, 'freports/detail_form.html', {'new_content': new_content, 'content': content, 'header': header})

@login_required(login_url='/login/')
def delete_detail(request, rid, did):
    report = Report.objects.get(pk=rid)
    detail = ReportEvents.objects.get(pk=did)
    content = u"Ви дійсно бажаєте видалити подію '%s' до провадження №%s/017?" % (detail.name, report.number)
    header = u"Видалення події '%s' до провадження №%s/017" % (detail.name, report.number)

    if request.method == 'GET':
        return render(request, 'freports/delete_form.html', {'report': report, 'content': content, 'header': header})

    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            current_detail = detail
            current_detail.delete()
            last_detail = ReportEvents.objects.filter(report=report).order_by('date').reverse()
            if len(last_detail) == 0 or last_detail[0].activate == True:
                report.active = True
                if report.executed == True:
                    report.executed = False
                    report.date_executed = None
                report.save()
            elif last_detail[0].activate == False:
                report.active = False
                if report.executed == True:
                    report.executed = False
                    report.date_executed = None
                report.save()
            messages.success(request, u"Подія '%s' до провадження №%s/017 успішно видалена" % (detail.name, report.number))
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення події '%s' до провадження №%s/017 скасоване" % (detail.name, report.number))

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

def valid_detail(request_info, report_id):
    errors = {}
    new_element = {}

    report = Report.objects.filter(pk=report_id)
    if len(report) != 1:
        errors['report'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше'
    else:
        new_element['report'] = report[0]

    name = request_info.get('name')
    if name in ['first_arrived', 'arrived', 'petition', 'bill', 'paid', 'schedule', 'inspected', 'done']:
        new_element['name'] = request_info.get('name')
    else:
        errors['name'] = u"На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше"

    date = request_info.get('date')
    if not date:
        errors['date'] = u"Дата події є обов'язковою"
    else:
        try:
            new_element['date'] = date
        except ValueError:
            errors['date'] = u"Введіть коректний формат дати"

    if name == 'first_arrived':
        decision_date = request_info.get('decision_date')
        if not decision_date:
            errors['decision_date'] = u"Дата винесення ухвали є обов'язковою"
        else:
            try:
                new_element['decision_date'] = decision_date
            except ValueError:
                errors['decision_date'] = u"Введіть коректний формат дати"

    if name in ['first_arrived', 'arrived']:
        received = request_info.get('received')
        if not received:
            errors['received'] = u"Інформація про отримані матеріали є обов'язковою"
        else:
            new_element['received'] = received

    if name in ['petition', 'bill', 'paid', 'done', 'inspected']:
        subspecies = request_info.get('subspecies')
        if not subspecies:
            errors['subspecies'] = u"Інформація про підтип події є обов'язковою"
        else:
            new_element['subspecies'] = subspecies

    if name in ['schedule']:
        time = request_info.get('time')
        if not time:
            errors['time'] = u"Дата та час огляду є обов'язковими"
        else:
            try:
                new_element['time'] = time
            except ValueError:
                errors['time'] = u"Введіть коректний формат дати та часу"

    if name == 'petition':
        necessary = request_info.get('necessary')
        if not necessary:
            errors['necessary'] = u"Інформація про зміст клопотання є обов'язковою"
        else:
            new_element['necessary'] = necessary

    if name == 'bill':
        cost = request_info.get('cost')
        if not cost:
            errors['cost'] = u"Інформація про вартість роботи є обов'язковою"
        else:
            try:
                new_element['cost'] = int(cost)
            except ValueError:
                errors['cost'] = u"Введіть вартість в числовому вигляді"
                new_element['cost'] = cost

    new_element['sending'] = request_info.get('sending')
    new_element['address'] = request_info.get('address', '')
    new_element['info'] = request_info.get('info')

    activate_true_list = ['first_arrived', 'arrived', 'paid', 'inspected']
    if name in activate_true_list:
        new_element['activate'] = True
    elif name == u'done':
        new_element['activate'] = 'executed'
    else:
        new_element['activate'] = False

    return {'errors': errors, 'data': new_element}

