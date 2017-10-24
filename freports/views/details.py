# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Report, ReportEvents, ReportParticipants

@login_required(login_url='/login/')
def details_list(request, rid):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(report=Report.objects.get(pk=rid)).order_by('date')
    participants = ReportParticipants.objects.filter(report=Report.objects.get(pk=rid))

    return render(request, 'freports/report_detail.html', {'details': details, 'report': report, 'participants': participants})

@login_required(login_url='/login/')
def add_detail(request, rid):
    report = Report.objects.get(pk=rid)
    header = u'Додавання події до провадження №%s/017' % report.number

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html', {'content': new_element, 'errors': errors})

            else:
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
        return render(request, 'freports/detail_form.html', {'header': header})

@login_required(login_url='/login/')
def edit_detail(request, rid, did):
    report = Report.objects.get(pk=rid)
    detail = ReportEvents.objects.get(pk=did)
    header = u"Редагування події '%s' до провадження №%s/017" % (detail.name, report.number)

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_data = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html', {'content': new_data, 'errors': errors})

            else:
                edit_detail = detail
                edit_detail.date = new_data['date']
                edit_detail.name = new_data['name']
                edit_detail.info = new_data['info']
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
        content = detail
        content.date = content.date.isoformat()
        return render(request, 'freports/detail_form.html', {'content': content, 'header': header})

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

    date = request_info.get('date')
    if not date:
        errors['date'] = u"Дата події є обов'язковою"
    else:
        try:
            new_element['date'] = date
        except ValueError:
            errors['date'] = u"Введіть коректний формат дати"

    name = request_info.get('name')
    if not name:
        errors['name'] = u"Назва події є обов'язковою"
    else:
        new_element['name'] = name

    new_element['info'] = request_info.get('info')

    activate = request_info.get('activate')
    new_element['activate'] = activate

    return {'errors': errors, 'data': new_element}

